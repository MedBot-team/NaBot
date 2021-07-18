import pandas as pd
from tqdm import tqdm
from ruamel import yaml


class nlu_generator():
    def __init__(self, med_dataset, nlp_file):
        super().__init__()
        df = pd.read_csv(med_dataset)
        self.medicines = list(df['medicine'])

        with open(nlp_file, 'r') as f:
            self.nlu_dict = yaml.load(f, Loader=yaml.RoundTripLoader)

    def __example_generator(self, medicine):
        examples = {'usage' : f'- I am looking for [{medicine}](drug) detail\n\
          - What is [{medicine}](drug)?\n',
                    'dosage' : f'- How should I take [{medicine}](drug)?\n',

                    'interaction' : f'- What other drugs will affect [{medicine}](drug)?\n\
          - What drugs should not be taken with [{medicine}](drug)?\n\
          - Which drugs have a drug interaction with [{medicine}](drug)?\n',

                    'sideeffects' : f'- What are [{medicine}](drug) side-effects?\n\
          - What are side-effects of [{medicine}](drug)\n\
          - What condition is a serious side effect of [{medicine}](drug) use?\n\
          - What are the dangers of [{medicine}](drug)?\n',

                    'avoid' : f'- What to avoid while taking [{medicine}](drug)?\n',

                    'warnings' : f'- When should you not take [{medicine}](drug)?\n'
        }
        return examples

    def __find_intent(self, key, nlu_dict):
        isthere = False
        end = len(nlu_dict['nlu'])
        for index, intent_dict in enumerate(nlu_dict['nlu']):
            if key == intent_dict['intent']:
                isthere = True
                return isthere, index
        return isthere, end

    def __block_generator(self, key, examples):
        inp = f"""\
        intent: {key}
        examples: |
          {examples[key]}
        """
        return inp

    def generate(self):
        # Change "medicines[:3]" to "medicines" to get the complete list
        for medicine in tqdm(self.medicines[:3]):
            examples = self.__example_generator(medicine)
            for key in examples.keys():
                isthere, index = self.__find_intent(key, self.nlu_dict)
                if isthere:
                    self.nlu_dict['nlu'][index]['examples'] += examples[key].replace('  ', '')
                else:
                    inp = self.__block_generator(key, examples)
                    code = yaml.load(inp, Loader=yaml.RoundTripLoader)
                    self.nlu_dict['nlu'].insert(1, code)

    def write_data(self, nlp_file):
        with open(nlp_file, 'w') as f:
                yaml.dump(self.nlu_dict, f, Dumper=yaml.RoundTripDumper)


def main():
    generator = nlu_generator('drugs_dataset.csv', 'data/nlu.yml')
    generator.generate()
    generator.write_data('nlu_new.yml')

if __name__ == "__main__":
    main()