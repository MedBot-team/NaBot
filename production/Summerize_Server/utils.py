from transformers import pipeline

class Summarization():
    def _init_(self):
        super(Summarization, self)._init_()

    # List of all available models in QA task
    def available_model(self):
        models = ["/media/zahra-linux/UBUNTU 18_0/Ali_QA/"]
        return models

    # Initialize QA model
    def model_init(self, model_name):
        self.model = pipeline("summarization", model=model_name)

    # Get the answer from QA model
    def get_answer(self, context):
        model_out = self.model(context)
        answer = model_out[0]['summary_text']
        
        return answer
