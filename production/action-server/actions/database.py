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
    
    def search_in_table(self, table, name):
        '''
        Searches the table for entries with similar name. 
        '''
        cursor = self.connection.cursor()
        cursor.execute(self.SEARCH.format(table=table), (f'%{name}%',))
        records = [item[0] for item in cursor.fetchall()]
        return records
    
    def retrieve_from_table(self, table, name, column):
        '''
        Retrieves information from table.
        '''
        cursor = self.connection.cursor()
        cursor.execute(self.RETRIEVE.format(column=column, table=table),(name,))
        records = [item[0] for item in cursor.fetchall()]
        return records