from decouple import config
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .intent_map import get_columns
from .database import DatabaseConnector
from rasa_sdk.events import SlotSet


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
              
        input_entity = self.get_entity(tracker=tracker)
        chosen_entity = tracker.get_slot('chosen_entity')        
        intent = tracker.get_slot('intent_name')

        if input_entity is not None:
            drugs = self.db.search_drug(input_entity)
            labs = self.db.search_lab(input_entity)
            
            candidates = drugs + labs
            
            if len(candidates)>1 and input_entity!=chosen_entity:
                buttons = [{"payload": "/choose_candidate{{\"entity_name\":\"{cnd}\", \"chosen_entity\":\"{cnd}\"}}".format(cnd=candidate),
                            "title": f"{candidate}"} for candidate in candidates]
                dispatcher.utter_message(
                    text=f'Which one do you mean?',
                    buttons = buttons,
                    button_type = 'vertical',
                    )  
                 
            elif drugs:
                columns = get_columns(intent, 'drug')
                if columns:
                    answer = self.db.retrieve_drug(column=columns[0], drug_name=input_entity)
                    dispatcher.utter_message(text=answer[0])
                else:
                    dispatcher.utter_message(response='utter_cant_answer')
                    
                
            elif labs:
                columns = get_columns(intent, 'lab')
                if columns:
                    answer = self.db.retrieve_drug(column=columns[0], drug_name=input_entity)
                    dispatcher.utter_message(text=answer[0])
                else:
                    dispatcher.utter_message(response='utter_cant_answer')
                
            else:
                
                dispatcher.utter_message(response='utter_not_found')
               
        else:
            print(6)
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