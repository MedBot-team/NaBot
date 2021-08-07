import re
import math
import MySQLdb
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine


class CSV2DB():
    def __init__(self, csv_path, password, database, 
                 table, host, user, port, columns):
    
        super(CSV2DB, self).__init__
        self.df = pd.read_csv(csv_path)
        self.columns = columns
        self.database = database
        self.table = table
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
        )

    def select_column(self):
        if self.columns is not None:
            self.df = self.df[self.columns]

    def rm_multi_newline(self):
        self.df = self.df.replace(r'\n+', '\n', regex=True)

    def norm_column_name(self):
        columns = [column.replace('?', '') for column in self.df.columns]
        columns = [re.sub('-| ', '_', column) for column in columns]
        self.df.columns = columns

    def check_length(self):
        df_length = self.df.astype('str').applymap(lambda x: len(x)).max()
        self.name_length = df_length.iloc[0]

        if max(df_length) > 65535:
            print(f'Error: Length of some fields in the "{df_length.idxmax()}" column is too large.\n\
This might cause you to lose some parts of your data during conversion\n\
Please use other dtypes than TEXT in to_sql command. Ex. MEDIUMTEXT or LONGTEXT')
            exit()

    def create_database(self):
        cursor = self.db.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")

    def create_engine(self):
        self.engine = create_engine(
            f"mysql+mysqldb://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?charset=utf8")

    def to_sql(self):
        self.df.to_sql(self.table, self.engine, if_exists='fail', index=True)

    def add_primary_key(self):
        with self.engine.connect() as con:
            con.execute(f'ALTER TABLE `{self.table}` ADD PRIMARY KEY (`index`);')

    def change_type(self):
        name_length = int(math.ceil(self.name_length / 500.0)) * 500
        name_column = self.df.columns[0]

        with self.engine.connect() as con:
            con.execute(f'ALTER TABLE `{self.table}` MODIFY `{name_column}` VARCHAR({name_length});')


