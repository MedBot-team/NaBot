import mysql.connector


class DatabaseConnector():
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                )
        
        self.SERACH_DRUG = "SELECT medicine FROM drugs WHERE medicine LIKE %s"
        self.SERACH_LAB = "SELECT Lab_test FROM labs WHERE Lab_test LIKE %s"
        self.RETRIEVE_DRUG = "SELECT {column} FROM drugs WHERE medicine = %s"
        self.RETRIEVE_LAB = "SELECT {column} FROM labs WHERE lab_test = %s"
    
    def search_drug(self, entity_name):
        cursor = self.connection.cursor()
        cursor.execute(self.SERACH_DRUG, (f'%{entity_name}%',))
        records = [item[0] for item in cursor.fetchall()]
        return records
    
    def search_lab(self, entity_name):
        cursor = self.connection.cursor()
        cursor.execute(self.SERACH_LAB, (f'%{entity_name}%',))
        records = [item[0] for item in cursor.fetchall()]
        return records
    
    def retrieve_lab(self, column, test_name):
        cursor = self.connection.cursor()
        cursor.execute(self.RETRIEVE_LAB.format(column=column), (test_name,))
        records = [item[0] for item in cursor.fetchall()]
        return records
    
    def retrieve_drug(self, column, drug_name):
        cursor = self.connection.cursor()
        cursor.execute(self.RETRIEVE_DRUG.format(column=column), (drug_name,))
        records = [item[0] for item in cursor.fetchall()]
        return records
    
