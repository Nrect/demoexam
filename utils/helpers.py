import time
import uuid

import pyodbc
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from utils.app_style import WINDOW_STYLE_ID
from utils.app_style import ICO

from utils.consts import connection_string

TYPES_FORM = ('Create', 'Update')

con = pyodbc.connect(connection_string)


def execute_query(query: str) -> list:
    cursor = con.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def create_update(query: str, fields: list):
    cursor = con.cursor()
    cursor.execute(query, fields)
    cursor.commit()


def get_all_manufactures() -> list:
    res = execute_query("SELECT Name FROM Manufacturer")
    manufacturer_list = [x[0] for x in res]
    return manufacturer_list


def show_message(title, message, function):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setWindowIcon(QIcon(ICO))
    msg.setText(title)
    msg.setIcon(QMessageBox.Question)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg.setDefaultButton(QMessageBox.No)
    msg.setInformativeText(message)

    msg.buttonClicked.connect(function)
    msg.exec_()


def show_error_message(detail, error_message='Произошла ошибка!'):
    msg = QMessageBox()
    msg.setWindowTitle('Ошибка')
    msg.setWindowIcon(QIcon(ICO))
    msg.setMinimumWidth(300)
    msg.setIcon(QMessageBox.Critical)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)
    msg.setText(error_message + '\t\t\t\t')
    msg.setDetailedText(str(detail))

    msg.exec_()


def uuid_generator():
    return str(uuid.uuid4())


def set_window_style(self):
    self.setObjectName(WINDOW_STYLE_ID)
    style = open('theme/style.css', 'r')
    style = style.read()
    self.setStyleSheet(style)


def load_data(sp):
    for i in range(1, 11):
        time.sleep(0.2)
        sp.showMessage(f"Загрузка данных... {i * 10}%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom,
                       QtCore.Qt.black)
