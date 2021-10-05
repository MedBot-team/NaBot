from abc import ABC, abstractmethod
from decouple import config
import requests
import json

from .utils import get_processor_conf


class Processor(ABC):
    '''
    Meta class for processors.
    '''
    @abstractmethod
    def __init__(self, host=None):
        pass
    
    @abstractmethod
    def process(self, tracker, context):
        pass

   
class NoProcessor(Processor):
    '''
    A processor that doesn't change the input context. 
    '''
    def __init__(self):
        pass
    
    def process(self, tracker, context):
        return context


class QAProcessor(Processor):
    '''
    Finds the answer of question in given context.
    '''
    def __init__(self, host):
        self.host = host
        self.api_key = config('QA_API_KEY')
        self.headers = {'Content-Type': 'application/json'}
    
    def process(self, tracker, context):    
        question = tracker.latest_message['text']
        payload = json.dumps({
            "question": question,
            "context": context,
            "api_key": self.api_key,
                })
        response = requests.request("POST",
                                    self.host,
                                    headers=self.headers,
                                    data=payload
                                    )
        response = response.json()['answer']
        return response
    
     
class SummarizerProcessor(Processor):
    '''
    Summarizes given context.
    '''
    def __init__(self, host):
        self.host = host
        self.api_key = config('SUMMARIZER_API_KEY')
        self.headers = {'Content-Type': 'application/json'}
        
    def process(self, tracker, context):
        payload = json.dumps({
            "context": context,
            "api_key": self.api_key,
                })
        response = requests.request("POST",
                                    self.host,
                                    headers=self.headers,
                                    data=payload
                                    )
        response = response.json()['summary']
        return response
            

def create_processor():
    '''
    Returns a processor object based on config file.
    '''
    conf = get_processor_conf()
    if conf['type']=='no_process':
        return NoProcessor()
    elif conf['type']=='QA':
        return QAProcessor(conf['host_url'])
    elif conf['type']=='summarizer':
        return SummarizerProcessor(conf['host_url'])