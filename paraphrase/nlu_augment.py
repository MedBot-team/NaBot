import re
from tqdm import tqdm
from ruamel import yaml
from paraphrase import wordtune


class DataAugment():
    def __init__(self, nlu_file, token, draft_id):
        super(DataAugment, self).__init__()
        self.token = token
        self.paraphrase = wordtune(token, draft_id)

        with open(nlu_file, 'r') as f:
            self.nlu_dict = yaml.load(f, Loader=yaml.RoundTripLoader)

    # Function to remove entity tags
    def __tag_remove(self, inp):
        entity_tag = ""
        entity = ""

        # Check if entity tags in input exist or not
        if inp.find("[") != -1:
            # entity and its tag
            entity_tag = inp[inp.find("["):inp.find(")")+1]
            # entity
            entity = inp[inp.find("[")+1:inp.find("]")]
            # remove tag from input. only entity exists in input
            inp = inp.replace(entity_tag, entity)

        return inp, entity_tag, entity

    # augment nlu.yml datas with wordtune suggestions
    def data_augment(self):
        for intent in tqdm(self.nlu_dict['nlu']):
            inps = intent['examples'].split('\n')[:-1]

            # give each intents examples to wordtune
            for inp in inps:
                # strip dash and space from example
                inp = inp[2:]
                # remove tags from words
                inp, entity_tag, entity = self.__tag_remove(inp)
                # paraphrase examples
                payload = self.paraphrase.payload_generator(inp)
                headers = self.paraphrase.headers_generator()
                response = self.paraphrase.requests(payload, headers)
                # list of wordtune suggestions
                suggestion_list = self.paraphrase.get_suggestion(response, inp)

                for suggestion in suggestion_list:
                    # add tags to each entity case insensitivly
                    prog = re.compile(re.escape(entity), re.IGNORECASE)
                    intent['examples'] += f'- {prog.sub(entity_tag, suggestion)}\n'

    # remove all lines without entity tags
    def data_clean(self):
        for intent in self.nlu_dict['nlu']:
            # exclude request_drug and request_lab intents. there is not entity tags in these intents examples
            if intent['intent'] not in ['request_drug', 'request_lab']:
                example_list = intent['examples'].split('\n')
                intent['examples'] = ''.join(
                    example+'\n' for example in example_list if "[" in example)

    # write nlu datas to the disk
    def write_data(self, out_name):
        with open(out_name, 'w') as f:
            yaml.dump(self.nlu_dict, f, Dumper=yaml.RoundTripDumper)


def main():
    token = 'YOUR_TOKEN'
    draftId = 'YOUR_Draft_Id'

    nlu_file = 'nlu.yml'
    output_file = 'nlu_augment.yml'
    cleaned_output_file = 'nlu_cleaned.yml'

    augment = DataAugment(nlu_file, token, draftId)
    # rephrase input examples with wordtune
    augment.data_augment()
    # write augmented data to the disk
    augment.write_data(output_file)
    # remove examples without tags.
    # manual remove preferred
    augment.data_clean()
    # write cleaned data to the disk
    augment.write_data(cleaned_output_file)


if __name__ == '__main__':
    main()
