import pandas as pd
from tqdm import tqdm
from ruamel import yaml


class nlu_generator():
    def __init__(self, mode, med_dataset):
        super().__init__()
        df = pd.read_csv(med_dataset)
        if mode == 'drug':
            col = 'medicine'
        else:
            col = 'Lab test'
        self.list = df[col].values
        self.mode = mode

    def __block_generator(self):
        inp = f"""\
version: "2.0"

nlu:

- lookup: {self.mode}
  examples: |
"""
        code = yaml.load(inp, Loader=yaml.RoundTripLoader)
        return code

    def generate(self):
        code = self.__block_generator()
        for item in tqdm(self.list):
            code['nlu'][0]['examples'] += f'- {item.lower()}\n'
        return code

    def write_data(self, code, nlu_file):
        with open(nlu_file, 'w') as f:
            yaml.dump(code, f, Dumper=yaml.RoundTripDumper)


def main():
    mode = 'drug'
    # mode = 'lab'
    generator = nlu_generator(mode, 'drugs_dataset.csv')
    # generator = nlu_generator(mode, 'medplus_labs.csv')
    code = generator.generate()
    generator.write_data(code, 'data/drug.yml')
    # generator.write_data(code, 'data/lab.yml')


if __name__ == "__main__":
    main()
