import pyodbc
from PyQt5 import QtCore, QtWidgets, QtSql, QtGui
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QGridLayout

from utils.consts import TABLE_PRODUCT
from utils.connection_string import connection_string
from utils.app_style import ICO
from ui.product_card import ElementCard
from utils.consts import connection_string
import sys


class ProductWindow(QWidget):
    def __init__(self, parent=None):
        super(ProductWindow, self).__init__(parent, QtCore.Qt.Window)
        self.initUI()

    def initUI(self):
        self.vbox = QVBoxLayout()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()

        self.layout = QGridLayout(self.scrollAreaWidgetContents)
        self.layout.setContentsMargins(10, 10, 10, 10)
        row = 0
        column = 0
        counter = 0

        con = pyodbc.connect(connection_string)
        cursor = con.cursor()
        cursor.execute('select * from Product ')
        product_list = cursor.fetchall()
        # for product in product_list:
        #     print(product)

        for product in product_list:
            counter += 1
            if counter % 4 == 1:
                row += 1
                column = 0
            card = ElementCard(product[0], str(int(product[1])) + ' руб.',
                               'Активно' if product[4] else 'Не активен')
            column += 1
            self.layout.addWidget(card, row, column)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.vbox.addWidget(self.scrollArea)
        self.setMinimumSize(1300, 700)
        self.setLayout(self.vbox)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = ProductWindow()
    main.show()
    sys.exit(app.exec_())
