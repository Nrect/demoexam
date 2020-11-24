from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QComboBox, QVBoxLayout, QApplication, QCheckBox, \
    QHBoxLayout, QPushButton, QTextEdit

from utils.helpers import set_window_style
from utils.helpers import TYPES_FORM, get_all_manufactures


class ProductForm(QWidget):
    def __init__(self, type_form, main_photo, name, cost, description, is_active, uuid, manufacturer):
        super().__init__()
        set_window_style(self)
        self.type_form = type_form
        self.product_main_photo = main_photo
        self.product_name = name
        self.product_cost = cost
        self.product_description = description
        self.product_is_active = is_active
        self.product_uuid = uuid
        self.product_manufacturer = manufacturer

        self.init_ui()

        # def __new__(cls):
        #     if not hasattr(cls, 'instance'):
        #         cls.instance = super(ProductForm, cls).__new__(cls)
        #     return cls.instance

    def init_ui(self):
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Кнопки
        btn_layout = QHBoxLayout()

        self.btn_submit = QPushButton('Подтвердить')
        self.btn_cancel = QPushButton('Отменить')
        self.btn_upload = QPushButton('Загрузить изображение')

        btn_layout.addWidget(self.btn_upload)
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_cancel)

        # Поля товара
        self.line_product_uuid = QLineEdit()
        self.line_product_name = QLineEdit()
        self.line_product_cost = QLineEdit()
        self.line_product_description = QTextEdit()
        self.line_product_main_photo = QLabel()

        self.line_product_manufacturer = QComboBox()
        self.line_product_manufacturer.addItems(get_all_manufactures())

        self.line_product_is_active = QCheckBox()

        # Заполнение полей товара
        if self.type_form == TYPES_FORM[1]:
            self.line_product_uuid.setText(self.product_uuid)
            self.line_product_uuid.setReadOnly(True)

            self.line_product_name.setText(self.product_name)
            self.line_product_cost.setText(self.product_cost)
            self.line_product_description.setText(self.product_description)
            # Фото
            pixam = QPixmap(self.product_main_photo)
            self.line_product_main_photo.setPixmap(pixam)
            self.line_product_main_photo.setFixedSize(100, 200)
            self.line_product_main_photo.setScaledContents(True)

            print(self.product_is_active)
            # Чекбокс
            if self.product_is_active == 'Активно':
                self.line_product_is_active.setChecked(True)
            else:
                self.line_product_is_active.setChecked(False)

            self.line_product_manufacturer.setCurrentText(self.product_manufacturer)

        # Добавление элементов
        form_layout.addRow(QLabel('Фото:'), self.line_product_main_photo)
        form_layout.addRow(QLabel('Идентификатор:'), self.line_product_uuid)
        form_layout.addRow(QLabel('Наименование:'), self.line_product_name)
        form_layout.addRow(QLabel('Стоимость:'), self.line_product_cost)
        form_layout.addRow(QLabel('Описание:'), self.line_product_description)
        form_layout.addRow(QLabel('Производитель:'), self.line_product_manufacturer)
        form_layout.addRow(QLabel('Активен?'), self.line_product_is_active)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)
        # Окно
        self.setLayout(main_layout)
        self.setMinimumSize(1200, 700)

    def show_window(self):
        self.show()
