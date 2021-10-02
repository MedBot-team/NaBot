from decouple import config
from typing import Any, Text, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from .retrievers import create_retriever
from .processors import create_processor
from .dispatchers import dispatch


class GetAnswer(Action):    
    def __init__(self):
        super().__init__() 
        
        # Creates retriever using config.yml 
        self.retriever = create_retriever()
         # Creates processor using config.yml
        self.processor = create_processor()
    
    def name(self):
        return "get_answer"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        context = self.retriever.retrieve(tracker)
        answer = self.processor.process(tracker, context)
        dispatch(tracker, dispatcher, answer)      