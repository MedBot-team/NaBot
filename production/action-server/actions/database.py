import mysql.connector


class DatabaseConnector():
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                )
        
        self.SEARCH = "SELECT name FROM {table} WHERE name LIKE %s"
        self.RETRIEVE = "SELECT {column} FROM {table} WHERE name = %s"
    
    def search_in_table(self, table, entity_name):
        cursor = self.connection.cursor()
        cursor.execute(self.SERACH.format(table=table), (f'%{entity_name}%',))
        records = [item[0] for item in cursor.fetchall()]
        return records
    
    def retrieve_from_table(self, table, name, column):
        cursor = self.connection.cursor()
        cursor.execute(self.RETRIEVE_LAB.format(column=column, table=table),(name,))