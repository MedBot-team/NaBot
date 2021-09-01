from transformers import pipeline
class QuestionAnswering():
    def __init__(self):
        super(QuestionAnswering, self).__init__()

    # List of all available models in QA task
    def available_model(self):
        models = [
            "ahotrod/albert_xxlargev1_squad2_512",
            "bert-large-uncased-whole-word-masking-finetuned-squad",
            "bert-large-cased-whole-word-masking-finetuned-squad",
            "mrm8488/squeezebert-finetuned-squadv2",
            "bigwiz83/sapbert-from-pubmedbert-squad2",
            "franklu/pubmed_bert_squadv2",
            "distilbert-base-uncased-distilled-squad",
            "distilbert-base-cased-distilled-squad",
            "allenai/longformer-large-4096-finetuned-triviaqa"]
        return models

    # Initialize QA model
    def model_init(self, model_name):
        self.model = pipeline(model = model_name, 
                              tokenizer = model_name, 
                              task="question-answering")

    # Get the answer from QA model
    def get_answer(self, question, context):
        model_out = self.model(question=question, 
                              truncation = True,
                              max_seq_len = 512,
                              context=context)
        answer = model_out['answer']
        start = model_out['start']
        end = model_out['end']
        
        return answer, start, end
