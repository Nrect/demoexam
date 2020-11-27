from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QGridLayout, QPushButton, QMainWindow, \
    QLineEdit, QCompleter, QComboBox

from ui.product_card import ElementCard
from ui.product_add_eddit import ProductForm
from ui.sale_history import HistoryWindow

from utils.helpers import set_window_style, execute_query, TYPES_FORM, get_all_manufactures


def get_manufacturer_items() -> list:
    res = execute_query("SELECT Name FROM Manufacturer")
    manufacturer_list = res
    return manufacturer_list


def get_product_photos(product: str) -> list:
    res = execute_query(f"SELECT PhotoPath FROM ProductPhoto WHERE ProductID = '{product}'")
    product_photo = res
    product_photo_list = [x[0] for x in product_photo]
    return product_photo_list


def get_product_attached_product(product: str) -> str:
    res = execute_query(f"select COUNT(*) from AttachedProduct where MainProductID = '{product}'")
    attached_product = res
    attached_product_count = str([x[0] for x in attached_product][0])
    return attached_product_count


def get_attached_products(product: str) -> list:
    res = execute_query(f"Select AttachedProductID from AttachedProduct where MainProductID = '{product}'")
    attached_products = res
    attached_products_list = [x[0] for x in attached_products]
    return attached_products_list


class ProductWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ProductWindow, self).__init__(parent)
        # self.setWindowModality(QtCore.Qt.WindowModality(2))
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

        self.manufacturer_items = get_manufacturer_items()
        self.product_photos = get_product_photos
        self.product_attached_products_count = get_product_attached_product

        self.init_ui()

    def init_ui(self):
        self.main_query = "select * from Product"
        self.filter_query = None
        self.decrease_indicator = None
        self.increase_indicator = None
        self.elements = 0

        vbox = QVBoxLayout()

        # Кнопки
        btn_container = QGridLayout()
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

        self.btn_add = QPushButton('Добавить товар')
        self.btn_add.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add.clicked.connect(self.open_product_form)

        self.btn_history = QPushButton('История продаж')
        self.btn_history.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_history.clicked.connect(self.open_sale_history)

        btn_container.addWidget(self.btn_cost_decrease, 0, 0)
        btn_container.addWidget(self.btn_cost_increase, 0, 1)
        btn_container.addWidget(self.btn_cancel, 0, 2)
        btn_container.addWidget(self.btn_history, 1, 2)
        btn_container.addWidget(self.btn_add, 1, 0, 1, 2)

        # Поиск
        self.searchbar = QLineEdit()
        self.searchbar.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.searchbar.setPlaceholderText('Поиск...')
        self.searchbar.setClearButtonEnabled(True)
        self.searchbar.textChanged.connect(self.update_display)

        # Фильтр Производитель
        self.manufacturer_combobox = QComboBox()
        self.manufacturer_combobox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.manufacturer_combobox.addItem('Все производители')
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
        self.show_product_cards(self.main_query)
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

        res = execute_query(sql_query)
        self.product_list = res

        self.title_list = []

        for product in self.product_list:
            counter += 1
            if counter % 4 == 1:
                row += 1
                column = 0
            card = ElementCard(product[0], self.product_attached_products_count(product[0]),
                               str(int(product[1])) + ' руб.',
                               product[3], self.product_photos(product[0]),
                               'Активно' if product[4] else 'Не активен', product[2], product[6], product[5],
                               get_attached_products(product[0]))
            column += 1
            self.card_layout.addWidget(card, row, column)
            self.title_list.append(product[0])

        # Всего товаров
        self.elements = self.card_layout.count()
        self.parent.statusBar().showMessage(f'Всего товаров: {str(self.elements)}')

    def manufacturer_combobox_select(self, text):
        self.remove_items()
        self.main_query = f"select * from Product where ManufacturerID = '{text}'"
        if text != 'Все производители':
            if self.decrease_indicator:
                self.filter_query = self.main_query + " order by -Cost"
            elif self.increase_indicator:
                self.filter_query = self.main_query + " order by Cost"
            else:
                self.filter_query = self.main_query
            self.show_product_cards(self.filter_query)
        else:
            self.main_query = f"select * from Product"
            self.show_product_cards(self.main_query)

    def show_product_increase(self):
        self.btn_cost_increase.setEnabled(False)
        self.btn_cost_decrease.setEnabled(True)
        self.decrease_indicator = False
        self.increase_indicator = True
        self.remove_items()
        self.filter_query = self.main_query + " order by Cost"
        self.show_product_cards(self.filter_query)
        self.btn_cost_increase.setStyleSheet('background-color: rgb(255, 74, 109);')
        self.btn_cost_decrease.setStyleSheet('background-color: rgb(225, 228, 255);color:black;')
        self.btn_cancel.setDisabled(False)

    def show_product_decrease(self):
        self.btn_cost_decrease.setEnabled(False)
        self.btn_cost_increase.setEnabled(True)
        self.increase_indicator = False
        self.decrease_indicator = True
        self.remove_items()
        self.filter_query = self.main_query + " order by -Cost"
        self.show_product_cards(self.filter_query)
        self.btn_cost_decrease.setStyleSheet('background-color: rgb(255, 74, 109);')
        self.btn_cost_increase.setStyleSheet('background-color: rgb(225, 228, 255);color:black;')
        self.btn_cancel.setDisabled(False)

    def clear_filter(self):
        self.btn_cost_decrease.setEnabled(True)
        self.btn_cost_increase.setEnabled(True)
        self.increase_indicator = False
        self.decrease_indicator = False
        self.remove_items()
        self.show_product_cards(self.main_query)
        self.btn_cancel.setDisabled(True)
        self.btn_cost_decrease.setStyleSheet('background-color: rgb(225, 228, 255);color:black;')
        self.btn_cost_increase.setStyleSheet('background-color: rgb(225, 228, 255);color:black;')

    def open_product_form(self):
        self.product_form = ProductForm(TYPES_FORM[0], '', '', '', '', '', '', '')
        self.product_form.setWindowTitle('Добавить товар')
        self.product_form.show_window()

    def open_sale_history(self):
        self.history_window = HistoryWindow()
        self.history_window.show_history()

    def update_display(self):
        search_text = self.searchbar.text()
        self.remove_items()
        if len(search_text) <= 0:
            self.manufacturer_combobox.setCurrentIndex(0)
        self.main_query = f"select * from Product where Title like '{search_text}%' or Description like '{search_text}%'"
        self.show_product_cards(self.main_query)

    def remove_items(self):
        for i in range(self.elements - 1, -1, -1):
            layoutItem = self.card_layout.itemAt(i)
            w = layoutItem.widget()
            if w:
                self.card_layout.removeWidget(w)
                w.setParent(None)
                w.deleteLater()
