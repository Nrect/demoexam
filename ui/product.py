import pyodbc

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QGridLayout, QPushButton, QMainWindow, \
    QApplication

from ui.product_card import ElementCard

from utils.consts import connection_string
from utils.helpers import set_window_style


class ProductWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ProductWindow, self).__init__(parent, QtCore.Qt.Window)
        self.setWindowModality(QtCore.Qt.WindowModality(2))
        self.init_ui()
        set_window_style(self)

    def init_ui(self):
        self.product_window_widget = ProductWindowWidget(self)
        self.statusBar().showMessage(self.product_window_widget.status_bar_meaasge)

        self.setCentralWidget(self.product_window_widget)
        self.move(300,100)

class ProductWindowWidget(QWidget):
    def __init__(self, parent):
        super(ProductWindowWidget, self).__init__(parent)
        self.init_ui()
        self.status_bar_meaasge = f'Всего: {self.card_layout.count()} товаров.'


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
        elements = self.card_layout.count()
        for i in range(elements - 1, -1, -1):
            layoutItem = self.card_layout.itemAt(i)
            w = layoutItem.widget()
            if w:
                self.card_layout.removeWidget(w)
                w.setParent(None)
                w.deleteLater()
