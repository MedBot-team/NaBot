import json
import mysql.connector
from datetime import datetime


class Monitoring():
    def __init__(self, host, user, password, database):
        super(Monitoring, self).__init__()
        # Connect to the MySQL server
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database)

    # Get list of events from database
    def get_events(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT intent_name, data \
FROM events \
WHERE type_name = 'user'")

        events = [item for item in list(cursor)]
        return events

    # Extract list of intents from database
    def get_intents(self, events):
        intents = [event[0] for event in events]
        return intents

    # Extract list of `data` from events
    def get_datas(self, events):
        datas = [event[1] for event in events]
        return datas

    # Convert data from string to python dictionary
    def __data2dict(self, data):
        json_acceptable_string = data.replace("'", "\"")
        dictionary = json.loads(json_acceptable_string)
        return dictionary

    # Get important variables from datas by parsing the data
    def get_variables(self, datas):
        intent_confidences = []
        entity_confidences = []
        timestamps = []
        input_channels = []
        entity_extractors = []

        for data in datas:
            dictionary = self.__data2dict(data)

            intent_confidences.append(
                dictionary['parse_data']['intent']['confidence'])

            timestamps.append(dictionary['timestamp'])
            input_channels.append(dictionary['input_channel'])

            entity_extractors += [entity['extractor']
                                  for entity in dictionary['parse_data']['entities']]

            entity_confidences += [entity['confidence_entity']
                                   for entity in dictionary['parse_data']['entities'] if 'confidence_entity' in entity.keys()]

        return intent_confidences, entity_confidences, timestamps, input_channels, entity_extractors

    # Convert timestamps to YYYY-MM-DD format
    def convert_date(self, timestamps):
        dates = [datetime.fromtimestamp(timestamp).strftime(
            '%Y-%m-%d') for timestamp in timestamps]
        return dates

    # Extract list of feedbacks from datas
    def get_feedbacks(self, intents):
        feedbacks = [intent for intent in intents if intent in [
            'good_response', 'bad_response']]
        return feedbacks        
