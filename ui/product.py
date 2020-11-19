import pyodbc

from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QGridLayout, QPushButton, QMainWindow, \
    QHBoxLayout, QLineEdit, QCompleter, QComboBox

from ui.product_card import ElementCard

from utils.consts import connection_string
from utils.helpers import set_window_style


def get_manufacturer_items():
    con = pyodbc.connect(connection_string)
    cursor = con.cursor()
    cursor.execute("select distinct ManufacturerID from Product ")
    manufacturer_list = cursor.fetchall()
    return manufacturer_list


class ProductWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ProductWindow, self).__init__(parent, QtCore.Qt.Window)
        self.setWindowModality(QtCore.Qt.WindowModality(2))
        self.init_ui()
        set_window_style(self)

    def init_ui(self):
        self.product_window_widget = ProductWindowWidget(self)

        self.setCentralWidget(self.product_window_widget)
        self.move(300, 100)


class ProductWindowWidget(QWidget):
    def __init__(self, parent):
        super(ProductWindowWidget, self).__init__(parent)
        self.parent = parent
        self.elements = 0
        self.manufacturer_items = get_manufacturer_items()
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()

        # Кнопки
        btn_container = QHBoxLayout()
        self.btn_cost_decrease = QPushButton('Цена по убываюнию')
        self.btn_cost_decrease.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cost_decrease.clicked.connect(self.show_product_decrease)

        self.btn_cost_increase = QPushButton('Цена по возрастанию')
        self.btn_cost_increase.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cost_increase.clicked.connect(self.show_product_increase)

        self.btn_cancel = QPushButton('Отменить')
        self.btn_cancel.setDisabled(True)
        self.btn_cancel.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel.clicked.connect(self.clear_filter)

        btn_container.addWidget(self.btn_cost_decrease)
        btn_container.addWidget(self.btn_cost_increase)
        btn_container.addWidget(self.btn_cancel)

        # Поиск
        self.searchbar = QLineEdit()
        self.searchbar.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.searchbar.setPlaceholderText('Поиск...')
        self.searchbar.setTextMargins(5, 2, 5, 2)
        self.searchbar.setClearButtonEnabled(True)
        self.searchbar.textChanged.connect(self.update_display)

        # Фильтр Производитель
        self.manufacturer_combobox = QComboBox()
        self.manufacturer_combobox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.manufacturer_combobox.addItem('Все производители')
        self.manufacturer_combobox.setStyleSheet(
            'QComboBox{font-size:22px;border:2px solid rgb(225, 228, 255);border-radius:5px;}')
        for manufacturer in self.manufacturer_items:
            self.manufacturer_combobox.addItem(manufacturer[0])
        self.manufacturer_combobox.activated[str].connect(self.manufacturer_combobox_select)

        # Скролл
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll__area_widget_contents = QWidget()

        # Контейнер карточек
        self.card_layout = QGridLayout(scroll__area_widget_contents)
        self.card_layout.setContentsMargins(10, 10, 10, 10)
        self.show_product_cards("select * from Product")
        scroll_area.setWidget(scroll__area_widget_contents)

        # Подскаски
        self.completer = QCompleter(self.title_list)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)
        self.completer.popup().setStyleSheet('font-size:25px;border:2px solid black;border-radius:5px;')

        # Добавление виджетов
        vbox.addWidget(self.searchbar)
        vbox.addWidget(self.manufacturer_combobox)
        vbox.addLayout(btn_container)
        vbox.addWidget(scroll_area)

        # Окно
        self.setMinimumSize(1300, 800)
        self.setLayout(vbox)

    def show_product_cards(self, sql_query):
        row = 0
        column = 0
        counter = 0

        con = pyodbc.connect(connection_string)
        cursor = con.cursor()
        cursor.execute(sql_query)
        self.product_list = cursor.fetchall()

        self.title_list = []

        for product in self.product_list:
            counter += 1
            if counter % 4 == 1:
                row += 1
                column = 0
            card = ElementCard(product[0], str(int(product[1])) + ' руб.',
                               'Активно' if product[4] else 'Не активен')
            column += 1
            self.card_layout.addWidget(card, row, column)
            self.title_list.append(product[0])
        # Всего элементов
        self.elements = self.card_layout.count()
        self.parent.statusBar().showMessage(f'Всего товаров: {str(self.elements)}')

    def manufacturer_combobox_select(self, text):
        self.remove_items()
        if text != 'Все производители':
            self.show_product_cards(f"select * from Product where ManufacturerID = '{text}'")
        else:
            self.show_product_cards(f"select * from Product")

    def show_product_increase(self):
        self.show_product_cards("select * from Product order by Cost")
        self.btn_cost_increase.setStyleSheet('background-color: rgb(255, 74, 109);')
        self.btn_cost_decrease.setStyleSheet('background-color: rgb(225, 228, 255);color:black;')
        self.btn_cancel.setDisabled(False)

    def show_product_decrease(self):
        self.show_product_cards("select * from Product order by -Cost")
        self.btn_cost_decrease.setStyleSheet('background-color: rgb(255, 74, 109);')
        self.btn_cost_increase.setStyleSheet('background-color: rgb(225, 228, 255);color:black;')
        self.btn_cancel.setDisabled(False)

    def clear_filter(self):
        self.show_product_cards("select * from Product")
        self.btn_cancel.setDisabled(True)
        self.btn_cost_decrease.setStyleSheet('background-color: rgb(225, 228, 255);color:black;')
        self.btn_cost_increase.setStyleSheet('background-color: rgb(225, 228, 255);color:black;')


    def update_display(self):
        search_text = self.searchbar.text()
        self.remove_items()
        self.show_product_cards(
            f"select * from Product where Title like '{search_text}%' or Description like '{search_text}%'")

    def remove_items(self):
        for i in range(self.elements - 1, -1, -1):
            layoutItem = self.card_layout.itemAt(i)
            w = layoutItem.widget()
            if w:
                self.card_layout.removeWidget(w)
                w.setParent(None)
                w.deleteLater()
