from transformers import pipeline
from ruamel import yaml


# Loads config from config.yml file
def load_conf():
    CONFIG_FILE_ADR = './config.yml'
    with open(CONFIG_FILE_ADR, 'r') as f:
        conf = yaml.load(f, Loader=yaml.RoundTripLoader)
    return conf

class Summarizer():
   # List of all available models in Summarizaition task
    def available_model(self):
        models = ["google/pegasus-xsum"]
        return models

    # Initialize Summarizaition model
    def model_init(self, model_name):
        self.model = pipeline("summarization", model=model_name)

    # Get the answer from Summarizaition model
    def get_summary(self, context):
        model_out = self.model(context)
        summary = model_out[0]['summary_text']
        
        return summary