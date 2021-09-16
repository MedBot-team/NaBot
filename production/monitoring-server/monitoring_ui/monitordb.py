import json
from datetime import datetime, timedelta
import psycopg2
from psycopg2 import OperationalError


class Monitoring:
    def __init__(self, db_name, db_user, db_password, db_host, db_port) -> None:
        super(Monitoring, self).__init__()
        # Connect to the MySQL server
        try:
            self.db = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    # Find number of days from user statement
    def __day_mapper(self, statement):
        day = {'Last 24 hour': 1,
               'Last week': 7,
               'Last month': 30}

        return day[statement]

    # Return timestamp of X days ago
    def __past_timestamp(self, past_days):
        delta = timedelta(days=past_days)
        now = datetime.now()
        past_time = now - delta
        past_timestamp = round(past_time.timestamp())
        return past_timestamp

    # Get list of events from database
    def get_events(self, statement):
        past_days = self.__day_mapper(statement)
        past_timestamp = self.__past_timestamp(past_days)

        cursor = self.db.cursor()

        cursor.execute(f"SELECT intent_name, data \
FROM events \
WHERE type_name = 'user' \
AND timestamp >= {past_timestamp};")

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
        # json_acceptable_string = data.replace("'", "\"")
        # dictionary = json.loads(json_acceptable_string)
        dictionary = json.loads(data)
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
                                  for entity in dictionary['parse_data']['entities'] if 'extractor' in entity.keys()]

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
    
    def get_questions(self, datas):
        questions = []
        for data in datas:
            dictionary = self.__data2dict(data)

            questions.append(dictionary['text'])
        
        return questions

