from abc import ABC, abstractmethod
from decouple import config

from .database import DatabaseConnector
from .utils import get_retriever_conf, get_columns

class Retriever(ABC):
    '''
    Meta class for retrievers.
    '''
    @abstractmethod
    def __init__():
        pass
    
    @abstractmethod
    def retrieve():
        pass
    
class SQLRetriever(Retriever):
    '''
    A retriever to retrieve information from database. Uses intent and extracted entity.
    '''
    def __init__(self, conf):
        host, user, database, self.tables = self.parse_conf(conf)
        # read password from .env
        password = config('SQL_PASSWORD')
        
        self.db = DatabaseConnector(host=host,
                                    user=user,
                                    password=password,
                                    database=database,
                                    )
    
    def retrieve(self, tracker):
        '''
        Retrieves information from database. Collects parameters from tracker.
        '''
        input_entity = self.get_entity(tracker=tracker)       
        intent = tracker.get_slot('intent_name')
        
        if input_entity is not None:
            tables_containing_entity = []
            for table in self.tables:
                rec = self.db.search_in_table(table, input_entity)
                if rec:
                    tables_containing_entity.append(table)
                    
            if tables_containing_entity:
                # For now in information is found in multiple tables or multiple
                # rows of table, just the first one is used, we're planning to 
                # make better use of multiple piece if inforamtion in future updates
                table = tables_containing_entity[0]  
                columns = get_columns(intent, table)
                if columns:
                    answer = self.collect_answer(table, input_entity, columns)
                    return answer
                else:
                    # Detected intent does not map to any of table's columns.
                    return '__CODE2__'
            else:
                # input_entity is not found in any of tables.
                return '__CODE1__'
        else:
            # input_entity in None
            return '__CODE0__'
            
            
           
    @staticmethod            
    def parse_conf(conf):
        '''
        Returns database information and list of tables.
        '''
        host = conf['host']
        user = conf['user']
        database = conf['database']
        tables = conf['tables']
        if not isinstance(tables, list):
            tables = [tables]
        return host, user, database, tables
    
    @staticmethod
    def get_entity(tracker):
        '''
        Returns the extracted entity. Prioritizes the last extractor in pipeline.
        '''
        entity = tracker.get_slot('entity_name')
        if isinstance(entity, list):
            return entity[-1]
        else:
            return entity    
        
    def collect_answer(self, table, name, columns):
        answers = []
        for column in columns:
            record = self.db.retrieve_from_table(table, name, column) #is a list
            answers.append(record[0])
        answer = ' '.join(answers)
        return answer
        
    
class  SemanticRetriever(Retriever):
    pass

def create_retriever():
    '''
    Returns a retriever object based on config file.
    '''
    conf = get_retriever_conf()
    if conf['type']=='SQL_table':
        return SQLRetriever(conf)
    elif conf['type']=='semantic':
        pass