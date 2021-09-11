import difflib
from dns.message import Message
import mysql.connector
from decouple import config
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class LabRetrieve(Action):

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
        
        self.button_type='inline'

    def name(self) -> Text:
        return "lab_retrieve"

    def intent_mapper(self, intent):
        intent_col = {'usage_lab': 'What_is_it_used_for',
                      'detail_lab': 'What_is_the_test',
                      'need_lab': 'Why_do_I_need_the_test',
                      'during_lab': 'What_happens_during_the_test',
                      'prepare_lab': 'Will_I_need_to_do_anything_to_prepare_for_the_test',
                      'risk_lab': 'Are_there_any_risks_to_the_test',
                      'result_lab': 'What_do_the_results_mean',
                      'any_detail_lab': 'Is_there_anything_else_I_need_to_know_about_the_test'}
        return intent_col[intent]
    
    def find_most_similar(self, name, name_list):
        exact_name = difflib.get_close_matches(name, name_list)
        return exact_name

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message_id = tracker.latest_message['message_id']
        like_buttons = [
                {"payload": "/good_response{{\"message_id\":\"{id}\"}}".format(id=message_id),
                 "title": "👍🏻"},
                {"payload": "/bad_response{{\"message_id\":\"{id}\"}}".format(id=message_id), 
                 "title": "👎🏻"},
                ]
        addition_button = [{"payload": "/addition_request{{\"message_id\":\"{id}\"}}".format(id=message_id), 
                            "title": "request addition to database"},]
        
        # Check if entity is recognized or not
        if not tracker.latest_message['entities']:
            dispatcher.utter_message(
        text = 'I\'m sorry. Unfortunately, I don\'t have that lab in my dataset yet',
        buttons = addition_button,
        button_type = self.button_type,)
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
        
        cursor = self.db.cursor()
        # Find list of similar lab test to the user input
        cursor.execute(f"SELECT Lab_test FROM {self.table}")
        labs_list = [item[0] for item in list(cursor)]
        labs = self.find_most_similar(lab_in.lower(), labs_list)

        # Check lab test does exist in dataset or not
        if len(labs) != 0:
            cursor.execute(f"SHOW COLUMNS \
                            FROM {self.table} \
                            LIKE '{col}';")
            # Check whether the question about the lab exists or not
            if len(list(cursor)) == 0:
                dispatcher.utter_message(
                text = 'I\'m sorry. Unfortunately, I\'m not aware of that yet.',
                buttons = addition_button,
                button_type = self.button_type,)
            else:
                cursor.execute(f"SELECT {col} \
                                FROM {self.table} \
                                WHERE Lab_test = '{labs[0]}';")

                reply = "".join(item[0]+'\n' for item in list(cursor))
                dispatcher.utter_message(
                    text = reply,
                    buttons = like_buttons,
                    button_type = self.button_type,
                    )
        else:
            dispatcher.utter_message(
            text = 'I\'m sorry. Unfortunately, I don\'t have that lab in my dataset yet',
            buttons = addition_button,
            button_type = self.button_type,)

        cursor.close()
        # self.db.close()
        return []