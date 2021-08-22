import difflib
import mysql.connector
from decouple import config
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .intent_map import intent_map

class Retrieve(Action):    
    def __init__(self) -> None:
        super().__init__() 

        password = config('MYSQL_DATASETS_ROOT_PASSWORD') 
        user = config('SQL_USER')
        host = config('DATASETS_DB_HOST')
        database = config('MYSQL_DATASETS_DATABASE')

        self.table = config('LAB_TABLE')
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database)
        self.like_buttons = [
                {"payload": "/good_response", "title": "👍🏻"},
                {"payload": "/bad_response", "title": "👎🏻"},
                ]
        self.addition_button = [{"payload": "/addition_request", 
                                 "title": "request addition to database"},]
        self.button_type='inline'
    
    def name(self) -> Text:
        return "retrieve"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # if tracker.get_intent_of_latest_message() == 'what_is':
        intent = tracker.latest_message['intent']['name']
        entity = tracker.get_slot('entity_name')
        dispatcher.utter_message(
            text = f'intent:{intent}, entity:{entity}',
            )
        