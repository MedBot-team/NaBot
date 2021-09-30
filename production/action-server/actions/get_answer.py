from decouple import config
from typing import Any, Text, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class GetAnswer(Action):    
    def __init__(self):
        super().__init__() 
        

    
    def name(self):
        return "get_answer"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        pass