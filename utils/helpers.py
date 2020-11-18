import time

from PyQt5 import QtCore

from utils.app_style import WINDOW_STYLE_ID


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
