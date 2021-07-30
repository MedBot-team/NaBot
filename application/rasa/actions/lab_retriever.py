import difflib
import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class LabRetrieve(Action):

    def name(self) -> Text:
        return "lab_retrieve"

    def intent_mapper(self, intent):
        intent_col = {'usage_lab': 'What is it used for',
                      'detail_lab': 'What is the test',
                      'need_lab': 'Why do I need the test',
                      'during_lab': 'What happens during the test?',
                      'prepare_lab': 'Will I need to do anything to prepare for the test?',
                      'risk_lab': 'Are there any risks to the test?',
                      'result_lab': 'What do the results mean?',
                      'any_detail_lab': 'Is there anything else I need to know about the test?'}
        return intent_col[intent]
    
    def find_most_similar(self, name, name_list):
        exact_name = difflib.get_close_matches(name, name_list)
        return exact_name

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        df = pd.read_csv('../../datasets/medplus_labs.csv')

        # Check if entity is recognized or not
        if not tracker.latest_message['entities']:
            dispatcher.utter_message(
        'I\'m sorry. Unfortunately, I don\'t have that lab in my dataset yet')
            return []

        # Check rasa forms are used or not
        if tracker.get_slot('lab') is None:
            intent = tracker.latest_message['intent']['name']
            col = self.intent_mapper(intent)
            lab_in = tracker.latest_message['entities'][-1]['value'].lower()
        else:
            col = 'What is the test'
            # Handling overlapping entities case
            if isinstance(tracker.get_slot('lab'), list):
                lab_in = tracker.get_slot('lab')[0].lower()
            else:
                lab_in = tracker.get_slot('lab').lower()

        # Find list of similar drugs to user input
        labs = self.find_most_similar(lab_in, df['Lab test'].values)
        # Check lab test does exist in dataset or not
        if len(labs) != 0:
            # Check whether the question about the lab exists or not
            if df[df['Lab test'] == labs[0]][col].isnull().values:
                dispatcher.utter_message(
                    'I\'m sorry. Unfortunately, I\'m not aware of that yet.')
            else:
                result = df[df['Lab test'] == labs[0]][col].values
                dispatcher.utter_message(result[0])
        else:
            dispatcher.utter_message(
                'I\'m sorry. Unfortunately, I don\'t have that lab in my dataset yet')
        return []
