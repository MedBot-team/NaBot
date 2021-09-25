import psycopg2
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration


class ChitChat():
    def __init__(self,
                 postgres_user=None,
                 postgres_password=None,
                 postgres_host=None,
                 postgres_port=None,
                 postgres_database=None):

        super(ChitChat, self).__init__()
        self.postgres_user = postgres_user
        self.postgres_password = postgres_password
        self.postgres_host = postgres_host
        self.postgres_port = postgres_port
        self.postgres_database = postgres_database

    def available_model(self):
        models = [
            "facebook/blenderbot-90M",
            "facebook/blenderbot_small-90M",
            "facebook/blenderbot-400M-distill",
            "facebook/blenderbot-1B-distill",
            "facebook/blenderbot-3B"
        ]
        return models

    def model_init(self, model_name):
        self.model = BlenderbotForConditionalGeneration.from_pretrained(
            model_name)
        self.tokenizer = BlenderbotTokenizer.from_pretrained(model_name)

    def get_reply(self, utterance):
        inputs = self.tokenizer([utterance], return_tensors='pt')
        reply_ids = self.model.generate(**inputs)
        reply = self.tokenizer.batch_decode(
            reply_ids, skip_special_tokens=True)[0]

        return reply

    def __create_connection(self):
        try:
            connection = psycopg2.connect(user=self.postgres_user,
                                          password=self.postgres_password,
                                          host=self.postgres_host,
                                          port=self.postgres_port,
                                          database=self.postgres_database)

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

        return connection

    def createdb(self, table_name):
        try:
            connection = self.__create_connection()
            cursor = connection.cursor()

            create_table_query = f'''CREATE TABLE IF NOT EXISTS {table_name}
                (ID SERIAL PRIMARY KEY     NOT NULL,
                MESSAGE         TEXT    NOT NULL,
                REPLY           TEXT    NOT NULL);'''

            cursor.execute(create_table_query)
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

    def updatedb(self, table_name, utterance, reply):
        try:
            connection = self.__create_connection()
            cursor = connection.cursor()

            sql_insert_query = f"""INSERT INTO {table_name} (MESSAGE, REPLY) 
                            VALUES (%s, %s)"""

            cursor.execute(sql_insert_query, (utterance, reply))
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print(f"Failed inserting record into {table_name} table {error}")

        finally:
            if connection:
                cursor.close()
                connection.close()
