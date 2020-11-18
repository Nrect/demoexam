import pyodbc
from PyQt5 import QtCore, QtWidgets, QtSql, QtGui
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QGridLayout, QPushButton

from utils.consts import TABLE_PRODUCT
from utils.connection_string import connection_string
from ui.product_card import ElementCard
from utils.app_style import ICO, WINDOW_STYLE_ID
from utils.consts import connection_string
import sys


class ProductWindow(QWidget):
    def __init__(self, parent=None):
        super(ProductWindow, self).__init__(parent, QtCore.Qt.Window)
        self.initUI()

    def initUI(self):
        self.setObjectName(WINDOW_STYLE_ID)
        style = open('theme/style.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

        self.vbox = QVBoxLayout()

        self.showBtn = QPushButton('Цена по убываюнию')
        self.showBtn.clicked.connect(self.show_product)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()

        self.layout = QGridLayout(self.scrollAreaWidgetContents)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.show_product_cards('select * from Product')

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Добавление виджетов
        self.vbox.addWidget(self.showBtn)

        self.vbox.addWidget(self.scrollArea)

        self.setMinimumSize(1300, 700)
        self.setLayout(self.vbox)

    def show_product_cards(self,sql_query):

        row = 0
        column = 0
        counter = 0

        con = pyodbc.connect(connection_string)
        cursor = con.cursor()
        cursor.execute(sql_query)
        product_list = cursor.fetchall()

        for product in product_list:
            counter += 1
            if counter % 4 == 1:
                row += 1
                column = 0
            card = ElementCard(product[0], str(int(product[1])) + ' руб.',
                               'Активно' if product[4] else 'Не активен')
            column += 1
            self.layout.addWidget(card, row, column)

    def show_product(self):
        self.show_product_cards('select * from Product order by -Cost')

    def remove_items(self):
        elements = self.layout.count()
        for i in range(elements - 1, -1, -1):
            layoutItem = self.layout.itemAt(i)
            w = layoutItem.widget()
            if w:
                self.layout.removeWidget(w)
                w.setParent(None)
                w.deleteLater()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = ProductWindow()
    main.show()
    sys.exit(app.exec_())
