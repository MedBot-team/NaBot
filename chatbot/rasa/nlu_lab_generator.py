import pandas as pd
from tqdm import tqdm
from ruamel import yaml


class nlu_generator():
    def __init__(self, lab_dataset, nlu_file):
        super().__init__()
        df = pd.read_csv(lab_dataset)
        self.labs = list(df['Lab test'])

        with open(nlu_file, 'r') as f:
            self.nlu_dict = yaml.load(f, Loader=yaml.RoundTripLoader)

    def __example_generator(self, lab):
        examples = {'inform_lab' : f'- [{lab}](lab)\n',
                    'usage_lab' : f'- What is the [{lab}](lab) used for?\n',
                    'detail_lab' : f'- What is the [{lab}](lab)?\n',
                    'need_lab' : f'- Why do I need the [{lab}](lab)?\n',
                    'during_lab' : f'- What happens during the [{lab}](lab)?\n',
                    'prepare_lab' : f'- Will I need to do anything to prepare for the [{lab}](lab)?\n',
                    'risk_lab' : f'- Are there any risks to the [{lab}](lab)?\n',
                    'result_lab' : f'- What do the [{lab}](lab) test results mean?\n',
                    'any_detail_lab' : f'- Is there anything else I need to know about the [{lab}](lab)?\n'
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
        # Change "labs[:3]" to "lab" to get the complete list
        for lab in tqdm(self.labs[:3]):
            examples = self.__example_generator(lab)
            for key in examples.keys():
                isthere, index = self.__find_intent(key, self.nlu_dict)
                if isthere:
                    self.nlu_dict['nlu'][index]['examples'] += examples[key].replace('  ', '')
                else:
                    inp = self.__block_generator(key, examples)
                    code = yaml.load(inp, Loader=yaml.RoundTripLoader)
                    self.nlu_dict['nlu'].insert(1, code)

    def write_data(self, nlu_file):
        with open(nlu_file, 'w') as f:
                yaml.dump(self.nlu_dict, f, Dumper=yaml.RoundTripDumper)


def main():
    generator = nlu_generator('medplus_labs.csv', 'data/nlu_default.yml')
    generator.generate()
    generator.write_data('data/nlu.yml')

if __name__ == "__main__":
    main() 
