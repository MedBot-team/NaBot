import re
import os
import time
import nltk
import json
import pandas as pd
import pandas as pd
from tqdm import tqdm
from rouge import Rouge
from typing import List
from spacy.lang.en import English
from haystack import Document
from haystack.reader import TransformersReader
from haystack.pipeline import ExtractiveQAPipeline
from haystack.retriever.dense import DensePassageRetriever
from haystack.document_store.faiss import FAISSDocumentStore
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction


nlp = English() 
nlp.add_pipe("sentencizer")


class report_generator():
    def __init__(self,
                 retriever_top_ks: list,
                 reader_top_ks: list,
                 embed_titles: list,
                 reader_models: list,
                 context_window_sizes: list,
                 text_datasets: list,
                 qa_datasets: list,
                 max_seq_len_passages: list,
                 max_seq_len_queries: list,
                 doc_strides: list,
                 max_seq_lens: list,
                 report_out_dir: str,
                 sample_out_dir: str):

        self.retriever_top_ks = retriever_top_ks
        self.reader_top_ks = reader_top_ks
        self.embed_titles = embed_titles
        self.doc_strides = doc_strides
        self.reader_models = reader_models
        self.context_window_sizes = context_window_sizes
        self.text_datasets = text_datasets
        self.qa_datasets = qa_datasets
        self.max_seq_len_passages = max_seq_len_passages
        self.max_seq_len_queries = max_seq_len_queries
        self.max_seq_lens = max_seq_lens
        self.report_out_dir = report_out_dir
        self.sample_out_dir = sample_out_dir
        self.columns = ['QA model', 'Dataset', 'embed_title', 'context_window_size',
                        'max_seq_len', 'doc_stride', 'max_seq_len_passage', 'max_seq_len_query',
                        'Retriever top-k', 'QA top-k', 'Rouge-1',
                        'Rouge-2', 'Rouge-l', 'Bleu',
                        'Answers percent in retrieved documents', 'VRAM',
                        'document embedding time', 'inference time'
                        ]

    def __load_dataset(self, qa_dataset, text_dataset):
        with open(qa_dataset, "r") as f:
            self.qa = json.loads(f.read())['data']
            df = pd.read_csv(text_dataset, index_col=0)
            df = df.reset_index()

        titles = list(df["title"].values)
        texts = list(df["text"].values)
        self.documents: List[Document] = []

        for title, text in zip(titles, texts):
            self.documents.append(
                Document(
                    text=text,
                    meta={
                        "name": title or ""
                    }
                )
            )

    def __init_doc_store(self, similarity="dot_product"):
        self.document_store = FAISSDocumentStore(similarity=similarity,
                                                 faiss_index_factory_str="Flat",
                                                 return_embedding=True
                                                 )

    def __init_retriever(self, embed_title,
                         query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
                         passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base"):

        self.retriever = DensePassageRetriever(document_store=self.document_store,
                                               query_embedding_model=query_embedding_model,
                                               passage_embedding_model=passage_embedding_model,
                                               use_gpu=True,
                                               embed_title=embed_title
                                               )

    def __update_embedding(self):
        self.document_store.delete_documents()
        self.document_store.write_documents(self.documents)
        self.document_store.update_embeddings(
            retriever=self.retriever
        )

    def __init_reader(self, model_name, window_size, seq_len, stride):
        self.reader = TransformersReader(model_name_or_path=model_name,
                                         context_window_size=window_size,
                                         max_seq_len=seq_len,
                                         doc_stride=stride,
                                         use_gpu=0
                                         )

    def __compute_metrics(self, reader, retriever, qa, retriever_top_k, reader_top_k):
        bleu_scores = []
        rouge1_scores = []
        rouge2_scores = []
        rougel_scores = []
        context_accuracy = []

        rouge = Rouge()
        smoothie = SmoothingFunction().method4

        for data in tqdm(qa):
            true_context = data['paragraphs'][0]['context']
            # true_context = true_context.replace('\n', ' ')

            for q_a in data['paragraphs'][0]['qas']:
                question = q_a['question']
                reference_list = set([answer['text']
                                     for answer in q_a['answers']])
                reference = " ".join(reference_list)
                reference_sents = nlp(reference)
                reference_sents = list(reference_sents.sents)
                reference_sents = [sent.text.lstrip().rstrip()
                                   for sent in reference_sents]

                pipe = ExtractiveQAPipeline(reader, retriever)

                preds = pipe.run(
                    query=question,
                    params={"Retriever": {"top_k": retriever_top_k},
                            "Reader": {"top_k": reader_top_k}}
                )

                candidate_sent_list = []

                for pred in preds['answers']:
                    pred_answer = pred['answer']

                    if pred_answer is not None:
                        offset_start = pred['offset_start']
                        offset_end = pred['offset_end']
                        meta_name = pred['meta']['vector_id']

                        pred_all_context_sents = []

                        for pred in preds['documents']:
                            pred_all_context_sents += list(
                                nlp(pred.to_dict()['text']).sents)

                            if pred.to_dict()['meta']['vector_id'] == meta_name:
                                pred_context = pred.to_dict()['text']
                                pred_context_sents = nlp(pred_context)
                                pred_context_sents = list(
                                    pred_context_sents.sents)
                                pred_context_sents = [
                                    sent.text for sent in pred_context_sents]
                                # pred_context = " ".join(pred_context_sents)

                        pred_all_context_sents = [
                            re.sub(r'\n+', ' ', sent.text).strip() for sent in pred_all_context_sents]

                        doc = nlp(pred_answer)
                        pred_answer_sents = list(doc.sents)
                        pred_answer_sents = [
                            sent.text for sent in pred_answer_sents]

                        for pred_context_sent in pred_context_sents:
                            start_index = 0
                            end_index = len(pred_answer)

                            for pred_answer_sent in pred_answer_sents:
                                right_reduction = len(
                                    pred_answer_sent) - len(pred_answer_sent.rstrip())
                                left_reduction = len(
                                    pred_answer_sent) - len(pred_answer_sent.lstrip())
                                end_index -= len(pred_answer_sent) + \
                                    0 if pred_context_sents[-1] == pred_answer_sent else 1

                                context_offset_start = pred_context.find(
                                    pred_context_sent)
                                context_offset_end = pred_context.find(
                                    pred_context_sent) + len(pred_context_sent)

                                if context_offset_start - left_reduction <= offset_start + start_index and context_offset_end + right_reduction >= offset_end - end_index:
                                    candidate_sent_list.append(
                                        pred_context_sent)

                                start_index += len(pred_answer_sent) + \
                                    0 if pred_context_sents[-1] == pred_answer_sent else 1

                        for reference_sent in reference_sents:
                            context_truth = 0

                            if reference_sent in pred_all_context_sents:
                                context_truth = 1

                            context_accuracy.append(context_truth)

                candidate_sent_set = set(candidate_sent_list)
                candidate = " ".join(candidate_sent_set)
                token_reference = nltk.word_tokenize(reference)
                token_candidate = nltk.word_tokenize(candidate)

                bleu_score = sentence_bleu(token_reference,
                                           token_candidate,
                                           smoothing_function=smoothie,
                                           weights=(1, 0, 0, 0))
                rouge_score = rouge.get_scores(candidate, reference)

                bleu_scores.append(bleu_score)
                rouge1_scores.append(rouge_score[0]['rouge-1']['f'])
                rouge2_scores.append(rouge_score[0]['rouge-2']['f'])
                rougel_scores.append(rouge_score[0]['rouge-l']['f'])

        ctx_acc = context_accuracy.count(1)/len(context_accuracy)
        bleu_ave = sum(bleu_scores)/len(bleu_scores)
        rouge1_ave = sum(rouge1_scores)/len(rouge1_scores)
        rouge2_ave = sum(rouge2_scores)/len(rouge2_scores)
        rougel_ave = sum(rougel_scores)/len(rougel_scores)
        # Pick the last question in dataset as a sample
        return bleu_ave, rouge1_ave, rouge2_ave, rougel_ave, ctx_acc, question, reference_list, true_context, candidate_sent_set, pred_all_context_sents

    def __serialize_sets(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return obj

    def get_report(self):
        logs = []
        metric = []

        self.__init_doc_store()

        for qa_dataset in self.qa_datasets:
            for text_dataset in self.text_datasets:
                self.__load_dataset(qa_dataset, text_dataset)

                for embed_title in self.embed_titles:
                    self.__init_retriever(embed_title)
                    tic = time.time()
                    self.__update_embedding()
                    toc = time.time()
                    document_embedding_time = toc - tic

                    for reader_model in self.reader_models:
                        for context_window_size in self.context_window_sizes:
                            for doc_stride in self.doc_strides:
                                for max_seq_len in self.max_seq_lens:
                                    self.__init_reader(
                                        reader_model, context_window_size, max_seq_len, doc_stride)

                                    for retriever_top_k in self.retriever_top_ks:
                                        for reader_top_k in self.reader_top_ks:
                                            for max_seq_len_passage in self.max_seq_len_passages:
                                                for max_seq_len_query in self.max_seq_len_queries:
                                                    tic = time.time()
                                                    bleu_ave, rouge1_ave, rouge2_ave, rougel_ave, ctx_acc, question, reference_list, true_context, candidate_sent_set, pred_all_context_sents = self.__compute_metrics(
                                                        self.reader, self.retriever, self.qa, retriever_top_k, reader_top_k)
                                                    toc = time.time()
                                                    inference_time = toc - tic

                                                    cmd = "nvidia-smi -q -x | grep \<fb_memory_usage\> -A 3 | grep used | sed -n 's:.*<used>\(.*\)</used>.*:\1:p'"
                                                    vram = os.system(cmd)

                                                    metric.append([reader_model, text_dataset, embed_title, context_window_size, max_seq_len, doc_stride,
                                                                   max_seq_len_passage, max_seq_len_query, retriever_top_k, reader_top_k, rouge1_ave,
                                                                   rouge2_ave, rougel_ave, bleu_ave, ctx_acc, vram, document_embedding_time, inference_time])

                                                    log = {'Question': question,
                                                           'Reference answers': reference_list,
                                                           'Reference context': true_context,
                                                           'Predicted answers': candidate_sent_set,
                                                           'Retrieved context': pred_all_context_sents
                                                           }

                                                    logs.append(log)

                    df = pd.DataFrame(metric, columns=self.columns)
                    df.to_csv(self.report_out_dir, index=False)

                    with open(self.sample_out_dir, 'w') as f:
                        json.dump(logs, f, default=self.__serialize_sets)

        return df, logs
