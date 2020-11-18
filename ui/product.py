import pyodbc

from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QGridLayout, QPushButton

from ui.product_card import ElementCard

from utils.consts import connection_string
from utils.helpers import set_window_style


class ProductWindow(QWidget):
    def __init__(self, parent=None):
        super(ProductWindow, self).__init__(parent, QtCore.Qt.Window)
        self.setWindowModality(QtCore.Qt.WindowModality(2))
        self.init_ui()
        set_window_style(self)

    def init_ui(self):
        vbox = QVBoxLayout()
        show_btn = QPushButton('Цена по убываюнию')
        show_btn.clicked.connect(self.show_product)
        # Скролл
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll__area_widget_contents = QWidget()
        # Контейнер карточек
        self.card_layout = QGridLayout(scroll__area_widget_contents)
        self.card_layout.setContentsMargins(10, 10, 10, 10)
        self.show_product_cards('select * from Product')
        scroll_area.setWidget(scroll__area_widget_contents)
        # Добавление виджетов
        vbox.addWidget(show_btn)
        vbox.addWidget(scroll_area)
        # Окно
        self.setMinimumSize(1300, 700)
        self.setLayout(vbox)

    def show_product_cards(self, sql_query):

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
            self.card_layout.addWidget(card, row, column)

    def show_product(self):
        self.show_product_cards('select * from Product order by -Cost')

    # ? мб пригодится
    def remove_items(self):
        elements = self.layout.count()
        for i in range(elements - 1, -1, -1):
            layoutItem = self.layout.itemAt(i)
            w = layoutItem.widget()
            if w:
                self.layout.removeWidget(w)
                w.setParent(None)
                w.deleteLater()
