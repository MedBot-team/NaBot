import difflib
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

    def find_most_similar(self, name, name_list):
        exact_name = difflib.get_close_matches(name, name_list)
        return exact_name

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        df = pd.read_csv('drugs_dataset.csv')

        # Check if entity is recognized or not
        if not tracker.latest_message['entities']:
            dispatcher.utter_message(
        'I\'m sorry. Unfortunately, I don\'t have that drug in my dataset yet')
            return []

        # Check rasa forms are used or not
        if tracker.get_slot('drug') is None:
            intent = tracker.latest_message['intent']['name']
            col = self.intent_mapper(intent)
            drug_in = tracker.latest_message['entities'][0]['value'].lower()
        else:
            col = 'uses'
            # Handling overlapping entities case
            if isinstance(tracker.get_slot('drug'), list):
                drug_in = tracker.get_slot('drug')[0].lower()
            else:
                drug_in = tracker.get_slot('drug').lower()

        # Find list of similar drugs to user input
        drugs = self.find_most_similar(drug_in, df['medicine'].values)
        # Check drug does exist in dataset or not
        if len(drugs) != 0:
            # Check whether the question about the drug exists or not
            if df[df['medicine'] == drugs[0]][col].isnull().values:
                dispatcher.utter_message(
                    'I\'m sorry. Unfortunately, I\'m not aware of that yet.')
            else:
                result = df[df['medicine'] == drugs[0]][col].values
                dispatcher.utter_message(result[0])
        else:
            dispatcher.utter_message(
                'I\'m sorry. Unfortunately, I don\'t have that drug in my dataset yet')
        return []
