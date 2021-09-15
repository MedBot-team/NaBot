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
    
    def name(self) -> Text:
        return "retrieve"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
              
        input_entity = self.get_entity(tracker=tracker)       
        intent = tracker.get_slot('intent_name')

        if input_entity is not None:
            drugs = self.db.search_drug(input_entity)
            labs = self.db.search_lab(input_entity)
            
            if drugs:
                message_id = tracker.latest_message['message_id']
                buttons = [
                    {"payload": "/good_response{{\"message_id\":\"{id}\"}}".format(id=message_id),
                    "title": "👍🏻"},
                    {"payload": "/bad_response{{\"message_id\":\"{id}\"}}".format(id=message_id), 
                    "title": "👎🏻"},
                    ]
                
                columns = get_columns(intent, 'drug')
                if columns:
                    answer = self.db.retrieve_drug(column=columns[0], drug_name=input_entity)
                    dispatcher.utter_message(text=answer[0],
                                             buttons=buttons,
                                             button_type='inline',
                                             )
                else:
                    dispatcher.utter_message(response='utter_cant_answer',
                                             buttons=buttons,
                                             button_type='inline',
                                             )
                    
                
            elif labs:
                message_id = tracker.latest_message['message_id']
                buttons = [
                    {"payload": "/good_response{{\"message_id\":\"{id}\"}}".format(id=message_id),
                    "title": "👍🏻"},
                    {"payload": "/bad_response{{\"message_id\":\"{id}\"}}".format(id=message_id), 
                    "title": "👎🏻"},
                    ]
                
                columns = get_columns(intent, 'lab')
                if columns:
                    answer = self.db.retrieve_lab(column=columns[0], test_name=input_entity)
                    dispatcher.utter_message(text=answer[0],
                                             buttons=buttons,
                                             button_type='inline',
                                             )
                else:
                    dispatcher.utter_message(response='utter_cant_answer',
                                             buttons=buttons,
                                             button_type='inline',
                                             )
                
            else:
                message_id = tracker.latest_message['message_id']
                button = [{"payload": "/addition_request{{\"message_id\":\"{id}\"}}".format(id=message_id), 
                            "title": "request addition to database"},]
                dispatcher.utter_message(response='utter_not_found',
                                         buttons=button,
                                         button_type='inline',
                                         )
               
        else:
            message_id = tracker.latest_message['message_id']
            button = [{"payload": "/addition_request{{\"message_id\":\"{id}\"}}".format(id=message_id), 
                        "title": "request addition to database"},]
            dispatcher.utter_message(response='utter_not_found',
                                        buttons=button,
                                        button_type='inline',
                                        )
    
    @staticmethod
    def get_entity(tracker: Tracker):
        entity = tracker.get_slot('entity_name')
        if isinstance(entity, list):
            return entity[-1]
        else:
            return entity