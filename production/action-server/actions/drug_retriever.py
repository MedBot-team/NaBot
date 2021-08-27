import difflib
import mysql.connector
from decouple import config
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class DrugRetrieve(Action):

    def __init__(self) -> None:
        super().__init__()  

        password = config('MYSQL_DATASETS_ROOT_PASSWORD') 
        user = config('SQL_USER')
        host = config('DATASETS_DB_HOST')
        database = config('MYSQL_DATASETS_DATABASE')

        self.table = config('DRUG_TABLE')
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
        return "drug_retrieve"

    def intent_mapper(self, intent):
        intent_col = {'usage_drug': 'uses',
                      'warnings_drug': 'warnings',
                      'dosage_drug': 'dosage',
                      'avoid_drug': 'what_to_avoid',
                      'sideeffects_drug': 'side_effects',
                      'interaction_drug': 'interactions'}
        return intent_col[intent]

    def find_most_similar(self, name, name_list):
        exact_name = difflib.get_close_matches(name, name_list)
        return exact_name

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Check if entity is recognized or not
        if not tracker.latest_message['entities']:
            dispatcher.utter_message(
               text = 'I\'m sorry. Unfortunately, I don\'t have that drug in my dataset yet',
               buttons = self.addition_button,
               button_type = self.button_type,
               )
            return []

        # Check rasa forms are used or not
        if tracker.get_slot('drug') is None:
            intent = tracker.latest_message['intent']['name']
            col = self.intent_mapper(intent)
            drug_in = tracker.latest_message['entities'][-1]['value'].lower()
        else:
            col = 'uses'
            # Handling overlapping entities case
            if isinstance(tracker.get_slot('drug'), list):
                drug_in = tracker.get_slot('drug')[0].lower()
            else:
                drug_in = tracker.get_slot('drug').lower()

        cursor = self.db.cursor()
        # Find list of similar drugs to the user input
        cursor.execute(f"SELECT medicine FROM {self.table}")
        drugs_list = [item[0] for item in list(cursor)]
        drugs = self.find_most_similar(drug_in.lower(), drugs_list)
        # Check drug does exist in dataset or not

        if len(drugs) != 0:
            cursor.execute(f"SHOW COLUMNS \
                            FROM {self.table} \
                            LIKE '{col}';")
            # Check whether the question about the drug exists or not
            if len(list(cursor)) == 0:
                dispatcher.utter_message(
                text = 'I\'m sorry. Unfortunately, I\'m not aware of that yet.',
                buttons = self.addition_button,
                button_type = self.button_type,)
            else:
                cursor.execute(f"SELECT {col} \
                                FROM {self.table} \
                                WHERE medicine = '{drugs[0]}';")

                reply = "".join(item[0]+'\n' for item in list(cursor))
                dispatcher.utter_message(
                    text = reply,
                    buttons = self.like_buttons,
                    button_type = self.button_type,)
        else:
            dispatcher.utter_message(
                text = 'I\'m sorry. Unfortunately, I don\'t have that drug in my dataset yet',
                buttons = self.addition_button,
                button_type = self.button_type,
                )
        
        cursor.close()
        # self.db.close()
        return []
