import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering


class QuestionAnswering():
    def __init__(self):
        super(QuestionAnswering, self).__init__()

    # List of all available models in QA task
    def available_model(self):
        models = [
            "allenai/longformer-large-4096-finetuned-triviaqa",
            "bert-large-uncased-whole-word-masking-finetuned-squad",
            "bert-large-cased-whole-word-masking-finetuned-squad",
            "distilbert-base-uncased-distilled-squad",
            "distilbert-base-cased-distilled-squad",
            "ahotrod/albert_xxlargev1_squad2_512",
            "roberta-large",
            "roberta-base"]
        return models

    # Initialize QA model
    def model_init(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = TFAutoModelForQuestionAnswering.from_pretrained(
            model_name)

    # Get the answer from QA model
    def get_answer(self, question, context):
        # Truncate tokens if they're larger than 512
        inputs = self.tokenizer.encode_plus(question,
                                            context,
                                            add_special_tokens=True,
                                            truncation=True,
                                            max_length=512,
                                            return_tensors="tf")

        input_ids = inputs["input_ids"].numpy()[0]
        # Get the answer start and end points
        answer_start_scores, answer_end_scores = self.model(inputs,
                                                            return_dict=False)

        answer_start = tf.argmax(answer_start_scores, axis=1).numpy()[0]
        answer_end = (tf.argmax(answer_end_scores, axis=1) + 1).numpy()[0]
        # Select the answer 
        answer = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
        return answer
