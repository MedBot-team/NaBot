import re
from ruamel import yaml
import numpy as np


def load_entities(entity_names):
    entities_dict = dict()
    for entity in entity_names:
        entity_file_adr = f'./{entity}.yml'
        entities_dict[entity] = load_entities_list(entity_file_adr)
    return entities_dict
 

def load_entities_list(file_adr):
    with open(file_adr, 'r') as f:
        entities = yaml.load(f, Loader=yaml.RoundTripLoader)
    entities = entities['nlu'][0]
    entities = entities['examples'].split('\n')
    entities = [row[2:] for row in entities]
    return entities


def randomize_entity_names(nlu_dict, entities_dict):
    for intent in nlu_dict['nlu']:
        examples = ''
        for example in intent['examples'].split('\n'):
            entity_match = dict()
            for entity in entities_dict:
                entity_match = re.search(f'\[[^\]]*\]\({entity}\)', example)
                if entity_match:
                    start, end = entity_match.span()
                    random_entity_name = f'[{np.random.choice(entities_dict[entity]).strip()}]({entity})'
                    example = example.replace(example[start:end] , random_entity_name)
                    
            examples += example + '\n'
        intent['examples'] = examples[:-1]  #removing last \n to avoid \n\n after the last example
    return nlu_dict



if __name__=='__main__':
    
    NLU_FILE = './nlu_cleaned.yml'
    ENTITY_NAMES = ['drug', 'lab'] #lookup files should be in same directoty as this file
    OUTPUT_FILE = 'nlu_random.yml'
    #load files
    with open(NLU_FILE, 'r') as f:
        nlu = yaml.load(f, Loader=yaml.RoundTripLoader)
    entities = load_entities(ENTITY_NAMES)

    randomized_nlu = randomize_entity_names(nlu, entities)
    #save
    with open(OUTPUT_FILE, 'w') as f:
        yaml.dump(randomized_nlu, f, Dumper=yaml.RoundTripDumper, default_flow_style=None)


    
    
    

    
    
    
    
    
    