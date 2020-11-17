from PyQt5 import QtSql


class MySqlConnection():
    def __init__(self, server, database, user='', password='', message=False):
        self.__SERVER_NAME = server
        self.__DATABASE_NAME = database
        self.__USERNAME = user
        self.__PASSWORD = password
        self.__message = message

    def create_connection(self):
        connection_string = f'DRIVER={{SQL Server}};' \
                            f'SERVER={self.__SERVER_NAME};' \
                            f'UID={self.__USERNAME};' \
                            f'PWD={self.__PASSWORD};' \
                            f'DATABASE={self.__DATABASE_NAME};'

        db = QtSql.QSqlDatabase.addDatabase('QODBC')
        db.setDatabaseName(connection_string)
        if db.open():
            if self.__message:
                print('Connection successful!')
            return db
        else:
            if self.__message:
                print(db.lastError().text())
            return False


