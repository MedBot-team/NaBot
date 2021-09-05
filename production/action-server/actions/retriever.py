import difflib
import mysql.connector
from decouple import config
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .intent_map import get_columns
from .database import DatabaseConnector

class Retrieve(Action):    
    def __init__(self) -> None:
        super().__init__() 

        password = config('MYSQL_DATASETS_ROOT_PASSWORD') 
        user = config('SQL_USER')
        host = config('DATASETS_DB_HOST')
        database = config('MYSQL_DATASETS_DATABASE')
        
        self.db = DatabaseConnector(host=host,
                                    user=user,
                                    password=password,
                                    database=database,
                                    )
        # self.like_buttons = [
        #         {"payload": "/good_response", "title": "👍🏻"},
        #         {"payload": "/bad_response", "title": "👎🏻"},
        #         ]
        # self.addition_button = [{"payload": "/addition_request", 
        #                          "title": "request addition to database"},]
        # self.button_type='inline'
    
    def name(self) -> Text:
        return "retrieve"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entity = self.get_entity(tracker=tracker)
        intent = tracker.get_slot('intent_name')
        
        if entity is not None:
            drugs = self.db.search_drug(entity)
            labs = self.db.search_lab(entity)
            if drugs and labs:
                dispatcher.utter_message(
                    text = 'entity is in both drug and lab',
                    )
            elif drugs:
                column = get_columns(intent, 'drug')[0]
                answer = self.db.retrieve_drug(column=column, drug_name=entity)
                print(entity)
                dispatcher.utter_message(text=answer[0])
            elif labs:
                column = get_columns(intent, 'lab')[0]
                answer = self.db.retrieve_lab(column=column, drug_name=entity)
                dispatcher.utter_message(text=answer[0])
            else:
                dispatcher.utter_message(response='utter_not_found')
               
        else:
            dispatcher.utter_message(response='utter_not_found')
        # dispatcher.utter_message(
        #     text = f'intent:{intent}, entity:{entity[-1]}',
        #     )
    
    @staticmethod
    def get_entity(tracker: Tracker):
        entity = tracker.get_slot('entity_name')
        if isinstance(entity, list):
            return entity[-1]
        else:
            return entity