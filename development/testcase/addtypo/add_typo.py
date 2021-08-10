import re
import string
import random
from ruamel import yaml


class AddTypo():
    def __init__(self):
        super().__init__()

    # Load the nlu datas
    def load_nlu(self, nlu_file):
        with open(nlu_file, 'r') as f:
            self.nlu_dict = yaml.load(f, Loader=yaml.RoundTripLoader)

    # Get all entity names
    def get_entities(self):
        # Find all strings between ]( and )
        entity_list = re.findall('(?<=]\()(.*?)(?=\))', yaml.dump(self.nlu_dict))
        entities = set(entity_list)
        return entities

    # Add typos in the single example
    def __example_typo(self, example, n, entities):
        # Find indices of non punctuation and nonspace characters
        inds = [i for i, letter in enumerate(
            example) if letter not in string.punctuation + ' ']
        inds_not_entity = inds
        # Find indices of strings in the entity tag. (Entity tags name should not change)
        
        for entity in entities:
            if f']({entity})' in example:
                # Find the index of the beginning of the entity tag
                start = example.index(f']({entity})')
                # Find the index of the end of the entity tag
                end = start + len(f']({entity})')
                # Find all indices which contains the entity tag
                entity_tag = list(range(start, end))
                # List of not entity tags. Remove all indices related to the entity tag
                inds_not_entity = list(set(inds_not_entity) - set(entity_tag))
        # Choose n sample(s) of the non entity tag indices
        sample = random.sample(inds_not_entity, n)

        typo_example = list(example)
        # Randomly substitute some letters of the string 
        for ind in sample:
            typo_example[ind] = random.choice(string.ascii_letters)
        # Return the wrong string
        return typo_example

    # Add a typo in all examples of the nlu key
    def nlu_typo(self, n, entities):
        # For loop in all intents, lookup tables and synonyms 
        for key in self.nlu_dict['nlu']:
            # Find all examples under intents, lookup tables and synonyms 
            examples = key['examples'].split('\n')[:-1]
            typo_examples = ""

            for example in examples:
                typo_example = self.__example_typo(example, n, entities)
                typo_examples += "".join(typo_example) + '\n'
            # Replace examples with their wrong ones
            key['examples'] = typo_examples

    # Save new yml file consists of the typo-contained examples
    def save_nlu(self, new_nlu_file):
        with open(new_nlu_file, 'w') as f:
            yaml.dump(self.nlu_dict, f, Dumper=yaml.RoundTripDumper)

