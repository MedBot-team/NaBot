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


class DrugRetrieve(Action):

    def name(self) -> Text:
        return "drug_retrieve"

    def intent_mapper(self, intent):
        intent_col = {'usage_drug': 'uses',
                      'warnings_drug': 'warnings',
                      'dosage_drug': 'dosage',
                      'avoid_drug': 'what-to-avoid',
                      'sideeffects_drug': 'side-effects',
                      'interaction_drug': 'interactions'}
        return intent_col[intent]

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        df = pd.read_csv('drugs_dataset.csv')

        # Check rasa forms are used or not
        if tracker.get_slot('drug') is None:
            intent = tracker.latest_message['intent']['name']
            col = self.intent_mapper(intent)
            drug = tracker.latest_message['entities'][0]['value'].lower()
        else:
            col = 'uses'
            drug = tracker.get_slot('drug').lower()

        # Check drug does exist in dataset or not
        if (df['medicine'] == drug).any():
            # Check whether the question about the drug exists or not
            if df[df['medicine'] == drug][col].isnull().values:
                dispatcher.utter_message(
                    'I\'m sorry. Unfortunately, I\'m not aware of that yet.')
            else:
                result = df[df['medicine'] == drug][col].values
                dispatcher.utter_message(result[0])
        else:
            dispatcher.utter_message(
                'I\'m sorry. Unfortunately, I don\'t have that drug in my dataset yet')
        return []
