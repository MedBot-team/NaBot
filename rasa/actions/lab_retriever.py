# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class LabRetrieve(Action):

    def name(self) -> Text:
        return "lab_retrieve"

    def intent_mapper(self, intent):
        intent_col = {'usage_lab':'What is it used for', 
                      'detail_lab':'What is the test', 
                      'need_lab':'Why do I need the test', 
                      'during_lab':'What happens during the test?',
                      'prepare_lab':'Will I need to do anything to prepare for the test?', 
                      'risk_lab':'Are there any risks to the test?',
                      'result_lab':'What do the results mean?',
                      'any_detail_lab':'Is there anything else I need to know about the test?'}
        return intent_col[intent]

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        lab = tracker.latest_message['entities'][0]['value']
        intent = tracker.latest_message['intent']['name']
        col = self.intent_mapper(intent)
        df = pd.read_csv('medplus_labs.csv')
        result = list(df[df['Lab test'] == lab][col])
        dispatcher.utter_message(result[0])
        
        return []


# from rasa_sdk.events import AllSlotsReset

# class ActionHelloWorld(Action):

#      def name(self) -> Text:
#             return "action_hello_world"

#      def run(self, dispatcher: CollectingDispatcher,
#              tracker: Tracker,
#              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#          dispatcher.utter_message("Hello World!")

#          return [AllSlotsReset()]
