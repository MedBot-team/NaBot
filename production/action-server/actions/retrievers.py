from abc import ABC, abstractmethod

from .intent_map import get_columns
from .database import DatabaseConnector


class retriever(ABC):
    '''
    Meta class for retrievers.
    '''
    @abstractmethod
    def __init__():
        pass
    
    @abstractmethod
    def get():
        pass
    
class sql_retriever(retriever):
    '''
    
    '''
    def __init__(self, conf):
        pass
    
    def get():
        pass

class  semantic_retriever(retriever):
    pass