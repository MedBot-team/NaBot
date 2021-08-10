from numpy.lib.function_base import extract
from requests import post
import json 
import re
from ruamel import yaml
from sklearn.metrics import classification_report, confusion_matrix
import os
import seaborn as sns
import matplotlib.pyplot as plt


def parse_example(text):
    entity_match = re.search('\[[^\]]*\]\([^\]]*\)', text) 
    if entity_match:
        entity_and_value = entity_match.group(0)
        value = re.search('\[[^\]]*\]', entity_and_value).group()[1:-1]
        entity = re.search('\]\([^\]]*\)', entity_and_value).group()[2:-1]
        text = text.replace(entity_and_value, value)
    else:
        value = None
        entity = None
        
    return text, entity, value


def collect_results(nlu):
    results = []
    for intent in nlu['nlu']:
        true_intent = intent['intent']
        for example in intent['examples'].split('\n')[:-1]:
            text, entity, value = parse_example(example[2:])
            data = f'{{"text": "{text}"}}'
            output = post('http://localhost:5005/model/parse', data=data)
            output = json.loads(output.text)
            top3 = output['intent_ranking'][:3]
            
            res = dict()
            if output['entities']:
                res['True entity'] = (entity, value) 
                res['extracted entity'] = (output['entities'][-1]['entity'],
                                           output['entities'][-1]['value']
                                           )
                if 'confidence_entity' in output['entities'][-1]:
                    res['extracted entity confidence'] = output['entities'][-1]['confidence_entity']
            elif entity:
                res['True entity'] = (entity, value)
                res['extracted entity'] =(None, None)
                
            res['example'] = text
            res['True intent'] = true_intent 
            top3_intents = []
            top3_confidences = []
            for pred in top3:
                top3_intents.append(pred['name'])
                top3_confidences.append(pred['confidence'])
            res['predicted intents'] = top3_intents
            res['intent confidences'] = top3_confidences
            results.append(res)
    return results


def create_intent_classification_report(results):
    preds = []
    trues =[]
    top3s = []
    for res in results:
        trues.append(res['True intent'])
        preds.append(res['predicted intents'][0])
        top3s.append(res['predicted intents'])

    with open(os.path.join(FILE_DIR, 'intent classification report.txt'), 'w') as f:
        f.write(classification_report(trues, preds))
    
    labels = list(set(trues))
    
    cm = confusion_matrix(trues, preds, labels=labels)
    fig, ax= plt.subplots(figsize=(20,20))
    sns.heatmap(cm, annot=True, fmt='g', ax=ax, cmap='Blues')
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Intent Confusion Matrix')
    ax.xaxis.set_ticklabels(labels, rotation=45) 
    ax.yaxis.set_ticklabels(labels, rotation=0)
    fig.savefig(os.path.join(FILE_DIR, 'intent confusion matrix.jpg'))
    
    create_top3_accuracy_report(top3s, preds)
    create_confidence_report(results)


def convert_None(text):
    if text is None:
        return 'None'
    else:
        return text

def create_top3_accuracy_report(top3s, preds):
    num_trues = 0
    for pred, top3 in zip(preds, top3s):
        if pred in top3:
            num_trues += 1
    with open(os.path.join(FILE_DIR, 'top3 report.txt'), 'w') as f:    
        f.write(f'top3 acc: {num_trues/len(preds)}')

def create_confidence_report(results):
    true_pred_confs = []
    wrong_pred_confs = []
    for res in results:
        if res['predicted intents'][0] == res['True intent']:
            true_pred_confs.append(res['intent confidences'][0])
        else:
            wrong_pred_confs.append(res['intent confidences'][0])
            
    fig, ax = plt.subplots(1, 2, figsize=(20, 12), sharey='all')
    ax = ax.flatten()
    ax[0].hist(true_pred_confs, facecolor='g')
    ax[0].set_title('True predictions')
    ax[1].hist(wrong_pred_confs, facecolor='r')
    ax[1].set_title('Wrong predictions')
    fig.suptitle('Histogram of confidence on Predictions')
    fig.savefig(os.path.join(FILE_DIR, 'intent confidence hist.jpg'))
    
      
def create_entity_classification_report(results):
    trues = []
    preds = []
    for res in results:
        if 'True entity' in res: 
            trues.append(res['True entity'][0])
            preds.append(res['extracted entity'][0])
    trues = [convert_None(label) for label in trues]
    preds = [convert_None(label) for label in preds]
    
    with open(os.path.join(FILE_DIR, 'entity classification report.txt'), 'w') as f:
        f.write(classification_report(trues, preds))
    
    labels = list(set(trues))
    
    cm = confusion_matrix(trues, preds, labels=labels)
    fig, ax= plt.subplots(figsize=(20,20))
    sns.heatmap(cm, annot=True, fmt='g', ax=ax, cmap='Blues')
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Entity Confusion Matrix')
    ax.xaxis.set_ticklabels(labels, rotation=45) 
    ax.yaxis.set_ticklabels(labels, rotation=0)
    fig.savefig(os.path.join(FILE_DIR, 'entity confusion matrix.jpg'))
    
   

if __name__ == '__main__':
    
    TEST_NLU_FILE = 'test_nlu.yml'
    FILE_DIR = os.path.dirname(__file__)
    TEST_NLU_FILE = os.path.join(FILE_DIR, TEST_NLU_FILE)

    with open(TEST_NLU_FILE, 'r') as f:
        test_nlu = yaml.load(f, Loader=yaml.RoundTripLoader)
    
    results = collect_results(test_nlu)
    
    create_intent_classification_report(results)
    create_entity_classification_report(results)