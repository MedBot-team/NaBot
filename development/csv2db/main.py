import sys
import argparse
import csv2db


def main(args):
    parser = argparse.ArgumentParser(description='To get arguments')

    parser.add_argument('-pa',
                        '--path',
                        type=str,
                        help='Path of the CSV file',
                        required=True)

    parser.add_argument('-ps',
                        '--password',
                        type=str,
                        help='MySQL password',
                        required=True)

    parser.add_argument('-db',
                        '--database',
                        type=str,
                        help='Database name',
                        required=True)

    parser.add_argument('-t',
                        '--table',
                        type=str,
                        help='Table name',
                        required=True)

    parser.add_argument('-ho',
                        '--host',
                        type=str,
                        default='127.0.0.1',
                        help='Host ip address',
                        required=False)

    parser.add_argument('-p',
                        '--port',
                        type=str,
                        default='3306',
                        help='Port of MySQL',
                        required=False)

    parser.add_argument('-u',
                        '--user',
                        type=str,
                        default='root',
                        help='MySQL user',
                        required=False)

    parser.add_argument('-c',
                        '--columns',
                        nargs='+',
                        type=str,
                        default=None,
                        help='Array of desired columns names. Default is all columns',
                        required=False)

    args = parser.parse_args()

    to_db = csv2db.CSV2DB(args.path,
                          args.password,
                          args.database,
                          args.table,
                          args.host,
                          args.user,
                          args.port,
                          args.columns)

    print('Select columns of dataframe')
    to_db.select_column()
    print('Remove redundant newlines')  
    to_db.rm_multi_newline()
    print('Modify columns name for database')  
    to_db.norm_column_name()
    print('Check strings length in the dataframe')  
    to_db.check_length()
    print('Create a new database')  
    to_db.create_database()
    print('Create a database engine')  
    to_db.create_engine()
    print('Convert dataframe to MySQL database')  
    to_db.to_sql()
    print('Add primary key to the database')  
    to_db.add_primary_key()
    print('Change name column type to VARCHAR from TEXT')  
    to_db.change_type()


if __name__ == '__main__':
    main(sys.argv[1:])
