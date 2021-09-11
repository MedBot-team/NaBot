#This file is to revise lookup tables
from ruamel import yaml


def load_table(table_adr):
    with open(table_adr, 'r') as f:
        entities = yaml.load(f, Loader=yaml.RoundTripLoader)
    entities = entities['nlu'][0]
    entities = entities['examples'].split('\n')
    entities = [row[2:] for row in entities]
    return entities

if __name__=='__main__':
    
    TABLES = ['./production/rasa-server/rasa/data/drug.yml',
              './production/rasa-server/rasa/data/lab.yml']
    
    for table in TABLES:
        entities = load_table(table)
        new_entities = [ent.replace('-',' ') for ent in entities if '-' in ent]
        with open (table, 'a') as f:
            for ent in new_entities:
                f.write(f'    - {ent}\n')