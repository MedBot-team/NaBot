from abc import ABC, abstractmethod

from .utils import get_processor_conf


class Processor(ABC):
    '''
    Meta class for processors.
    '''
    @abstractmethod
    def __init__():
        pass
    
    @abstractmethod
    def process(self, tracker, context):
        pass
    
class NoProcessor(Processor):
    '''
    A processor that doesn't change the input context. 
    '''
    def process(self, tracker, context):
        return context

def create_processor():
    '''
    Returns a processor object based on config file.
    '''
    conf = get_processor_conf()
    if conf['type']=='no_process':
        return NoProcessor()