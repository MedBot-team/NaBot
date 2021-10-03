from transformers import pipeline

class Summarization():
    def _init_(self):
        super(Summarization, self)._init_()

    # List of all available models in Summarizaition task
    def available_model(self):
        models = ["google/pegasus-xsum"]
        return models

    # Initialize Summarizaition model
    def model_init(self, model_name):
        self.model = pipeline("summarization", model=model_name)

    # Get the answer from Summarizaition model
    def get_summarizaition(self, context):
        model_out = self.model(context)
        summary = model_out[0]['summary_text']
        
        return summary
