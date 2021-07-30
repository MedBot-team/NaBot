import ast
import pandas as pd
from tqdm import tqdm
from ruamel import yaml


class nlu_generator():
    def __init__(self, mode, med_dataset):
        super().__init__()
        df = pd.read_csv(med_dataset)
        if mode == 'drug':
            col = 'drug_name'
            aka_col = 'Brand names'
        else:
            col = 'Lab test'
            aka_col = 'Also Known As'
        self.list = df[col].str.lower()
        aka_list = df[aka_col].str.lower()
        self.aka_list = aka_list.str.replace('®', '')
        self.mode = mode

    # Synonym key generator
    def __syn_generator(self, item, aka_list):
        inp = f"""\
nlu:
- synonym: {item}
  examples: |
"""
        code = yaml.load(inp, Loader=yaml.RoundTripLoader)
        if self.mode == 'lab':
            aka_list = ast.literal_eval(aka_list)
        else:
            aka_list = [aka_list]
        for aka in aka_list:
            code['nlu'][0]['examples'] += f'- {aka}\n'
        return code

    # First keys generator
    def __block_generator(self):
        inp = f"""\
version: "2.0"

nlu:
"""
        code = yaml.load(inp, Loader=yaml.RoundTripLoader)
        code['nlu'] = self.__syn_generator(
            self.list[0], self.aka_list[0])['nlu']
        return code

    # NaN check
    def __isnan(self, num):
        isnan = (num != num)
        return isnan

    # YAML generator
    def generate(self):
        # Generate first keys
        code = self.__block_generator()
        for i, item in tqdm(enumerate(self.list[1:], start=1)):
            # Check if aka_list for that item exists or not
            if not self.__isnan(self.aka_list[i]):
                # Append aka_list to YAML
                code['nlu'].append(self.__syn_generator(
                    item, self.aka_list[i])['nlu'][0])
        return code

    # Write data in the disk
    def write_data(self, code, nlu_file):
        with open(nlu_file, 'w') as f:
            yaml.dump(code, f, Dumper=yaml.RoundTripDumper)


def main():
    mode = 'lab'
    #mode = 'drug'
    generator = nlu_generator(
        mode, '../labtestonline_datasets/dataset_files/labtest_dataset.csv')
    #generator = nlu_generator(
        #mode, '../medlineplus_drug_dataset/dataset_files/MedlinePlus_2.csv')
    code = generator.generate()
    generator.write_data(code, 'data/synonym_lab.yml')
    #generator.write_data(code, 'data/synonym_drug.yml')


if __name__ == "__main__":
    main()
