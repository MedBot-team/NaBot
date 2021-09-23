from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration


class ChitChat():
    def __init__(self):
        super(ChitChat, self).__init__()

    def available_model(self):
        models = [
            "facebook/blenderbot-90M",
            "facebook/blenderbot_small-90M",
            "facebook/blenderbot-400M-distill",
            "facebook/blenderbot-1B-distill",
            "facebook/blenderbot-3B"
            ]
        return models

    def model_init(self, model_name):
        self.model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = BlenderbotTokenizer.from_pretrained(model_name)

    def get_reply(self, utterance):
        inputs = self.tokenizer([utterance], return_tensors='pt')
        reply_ids = self.model.generate(**inputs)
        reply = self.tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]

        return reply
