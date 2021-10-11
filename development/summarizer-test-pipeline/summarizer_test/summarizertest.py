import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import List, Union
import json
from tqdm import tqdm


class ReportGenerator():
    def __init__(self,
                 models_names: List[str],
                 val_contexts_path: str,
                 report_path: str,
                 max_lengths: list,
                 min_lengths: list,
                 top_k: list,
                 penalty_l: list,
                 no_repeat_ngram_size: list,
                 num_return_sequences: list,
                 ):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.models_names = models_names
        self.val_contexts_path = val_contexts_path
        self.report_path = report_path
        self.max_lengths = max_lengths
        self.min_lengths = min_lengths
        self.top_k = top_k
        self.penalty_l = penalty_l
        self.no_repeat_ngram_size = no_repeat_ngram_size
        self.num_return_sequences = num_return_sequences

    def __load_json_data(self, path: str):
        with open(path, 'r') as json_file:
            ds = json.load(json_file)
        return ds

    def __write_json_data(self, path: str, data: Union[list, dict]):
        with open(path, 'w') as f:
            json.dump(data, f)

    def __init_tokenizer(self, model: str):
        return AutoTokenizer.from_pretrained(model)

    def __init_model(self, model: str):
        return AutoModelForSeq2SeqLM.from_pretrained(model).to(self.device)

    def __summerize(self, text: str, tokenizer, model, min_l, max_l, top_k, penalty_l, no_repeat_ngram_size, num_return_sequences):
        inputs = tokenizer(
            [text], 
            padding="max_length",
            truncation=True, 
            max_length=512, 
            return_tensors="pt",
            )
        input_ids = inputs.input_ids.to(self.device)
        attention_mask = inputs.attention_mask.to(self.device)
        output = model.generate(
            input_ids,
            attention_mask=attention_mask,
            min_length=min_l,
            max_length=max_l,
            num_beams=1,
            length_penalty=penalty_l,
            early_stopping=True,
            no_repeat_ngram_size=no_repeat_ngram_size,
            num_return_sequences=num_return_sequences,
            do_sample=True,
            top_k=top_k,
            top_p=None,
            output_scores=True,
            return_dict_in_generate=True,
        )

        return [tokenizer.decode(ans, skip_special_tokens=True) for ans in output[0]]

    def get_report(self):
        print(f'{self.device} is available')
        self.__val_data = self.__load_json_data(self.val_contexts_path)
        self.logs = []
        for ckpt in self.models_names:
            print(f'start "{ckpt}" model')

            self.tokenizer = self.__init_tokenizer(ckpt)
            self.model = self.__init_model(ckpt)
            log = []
            for context in tqdm(self.__val_data):
                for maxl in self.max_lengths:
                    for minl in self.min_lengths:
                        for tk in self.top_k:
                            for pl in self.penalty_l:
                                for nrns in self.no_repeat_ngram_size:
                                    for nrs in self.num_return_sequences:
                                        summerized = self.__summerize(
                                            context['context'], self.tokenizer, self.model, minl, maxl, tk, pl, nrns, nrs)
                                        log.append({
                                            'summary': summerized,
                                            'context': context['context'],
                                            'max_length': maxl,
                                            'min_length': minl,
                                            'top_k': tk,
                                            'penalty_length': pl,
                                            'bo_repeat_ngram_size': nrns,
                                            'num_return_sequences': nrs,
                                        })
            self.logs.append({'model': ckpt, 'log': log})

        self.__write_json_data(self.report_path, self.logs)
        print(f"report saved into {self.report_path}")
