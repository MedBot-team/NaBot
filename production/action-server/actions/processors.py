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
    def process(self, context, tracker):
        pass
    
class NoProcessor(Processor):
    '''
    A processor that doesn't change the input context. 
    '''
    def process(self, context, tracker):
        return context
