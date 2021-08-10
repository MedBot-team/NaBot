from ruamel import yaml
from ruamel.yaml.comments import CommentedMap as OrderedDict
import random
from copy import deepcopy


def split(nlu, test_ratio):
    test_nlu = OrderedDict()
    train_nlu = OrderedDict()
    test_nlu['version'] = nlu['version']      
    train_nlu['version'] = nlu['version'] 
    test_nlu['nlu'] = deepcopy(nlu['nlu'])
    train_nlu['nlu'] = deepcopy(nlu['nlu'])
    
    for i in range(len(nlu['nlu'])):
        all_examples = nlu['nlu'][i]['examples'].split('\n')[:-1]
        num_test_examples = int(test_ratio * len(all_examples))
        test_examples = random.sample(all_examples, num_test_examples)
        train_examples = [example for example in all_examples if example not in test_examples]
        test_nlu['nlu'][i]['examples'] = '\n'.join(test_examples) + '\n'
        train_nlu['nlu'][i]['examples'] = '\n'.join(train_examples) + '\n'  
        
    return train_nlu, test_nlu


if __name__ == '__main__':

    NLU_FILE = './nlu_random.yml'
    TEST_RATIO = 0.2

    with open(NLU_FILE, 'r') as f:
            nlu = yaml.load(f, Loader=yaml.RoundTripLoader)

    train_nlu, test_nlu = split(nlu, TEST_RATIO)  
        
    with open('./test_nlu.yml', 'w') as f:
        yaml.dump(test_nlu, f, Dumper=yaml.RoundTripDumper)

    with open('./train_nlu.yml', 'w') as f:
        yaml.dump(train_nlu, f, Dumper=yaml.RoundTripDumper)
