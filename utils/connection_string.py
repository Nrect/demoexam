from utils.connection import MySqlConnection
from utils.consts import (SERVER_NAME, DATABASE_NAME, USER_NAME, USER_PASSWORD)

connection_string = MySqlConnection(SERVER_NAME, DATABASE_NAME, USER_NAME, USER_PASSWORD, message=True)
