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


class DataFrameRetrieve(Action):

    def name(self) -> Text:
        return "data_frame_retrieve"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        drug = tracker.get_slot('drug')
        intent = tracker.latest_message['intent']
        df = pd.read_csv('drugs_dataset.csv')
        result = df[df['medicine'] == drug][intent]

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