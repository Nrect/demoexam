import os
import shutil

from PyQt5.QtGui import QPixmap, QIcon, QDoubleValidator
from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QComboBox, QVBoxLayout, QApplication, QCheckBox, \
    QHBoxLayout, QPushButton, QTextEdit, QFileDialog, QGridLayout

from utils.app_style import ICO
from utils.helpers import set_window_style
from utils.helpers import TYPES_FORM, get_all_manufactures, uuid_generator, show_error_message, create_update


class ProductForm(QWidget):
    def __init__(self, type_form, main_photo, name, cost, description, is_active, uuid, manufacturer):
        super().__init__()
        set_window_style(self)
        self.type_form = type_form
        self.product_main_photo = main_photo
        self.product_name = name

        self.product_cost = cost.split(' ')[0]

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
        self.product_window = ProductWindowWidget()
        self.imagePath = ''
        main_layout = QGridLayout()
        form_layout = QFormLayout()

        # Кнопки
        btn_layout = QHBoxLayout()

        self.btn_submit = QPushButton('Подтвердить')
        self.btn_submit.clicked.connect(self.submit_form)

        self.btn_cancel = QPushButton('Отменить')
        self.btn_cancel.clicked.connect(self.cancel_form)

        self.btn_upload = QPushButton('Загрузить изображение')
        self.btn_upload.clicked.connect(self.upload_image)

        btn_layout.addWidget(self.btn_upload)
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_cancel)

        # Поля товара
        self.line_product_uuid = QLineEdit()
        self.line_product_uuid.setText(uuid_generator())

        self.line_product_name = QLineEdit()

        self.line_product_cost = QLineEdit()
        self.line_product_cost.setValidator(QDoubleValidator(1.00, 9999999.00, 2))

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
            self.line_product_main_photo.setFixedSize(300, 300)
            self.line_product_main_photo.setScaledContents(True)

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

        main_layout.addLayout(form_layout, 0, 0)
        main_layout.addLayout(btn_layout, 1, 0)
        # Окно
        self.setLayout(main_layout)
        self.setMinimumSize(1200, 700)
        self.setWindowIcon(QIcon(ICO))

    def show_window(self):
        self.show()

    def upload_image(self):
        file_name = QFileDialog.getOpenFileName(self, 'Выберите изображение', 'C:/', "Image files (*.jpg *.png)")
        try:
            self.imagePath = file_name[0]
            if self.imagePath:
                # ? Если картинка меньше 2мб, добавляем. Иначе выдаем ошибку
                image_size = os.path.getsize(self.imagePath) / 1024 / 1024
                if image_size <= 2:
                    self.image_name = "Товары салона красоты\\" + str(self.imagePath).split('/')[-1]
                    self.product_main_photo = self.image_name
                    pixmap = QPixmap(self.imagePath)
                    self.line_product_main_photo.setPixmap(pixmap)
                    self.line_product_main_photo.setFixedSize(300, 300)
                    self.line_product_main_photo.setScaledContents(True)
                else:
                    self.imagePath = ''
                    show_error_message('Превышен размер изображения', 'Изображение весит больше 2мб')
        except Exception as e:
            print(e)

    def submit_form(self):
        try:
            if self.imagePath:
                destination = os.path.abspath('./Товары салона красоты')
                shutil.copy(self.imagePath, destination)

            product_fields = [self.line_product_name.text(), float(self.line_product_cost.text()),
                              self.line_product_description.toPlainText(), self.product_main_photo,
                              self.line_product_is_active.isChecked(), self.line_product_manufacturer.currentText(),
                              self.line_product_uuid.text()]

            if self.type_form == TYPES_FORM[0]:
                create_update(
                    f"INSERT INTO Product(Title, Cost, Description, MainImagePath, IsActive, ManufacturerID, UUID) \
                    VALUES(?,?,?,?,?,?,?)", product_fields)
                self.product_window.show_product_cards("select * from Product")
            if self.type_form == TYPES_FORM[1]:
                pass
            self.cancel_form()
        except Exception as e:
            print(e)

    def cancel_form(self):
        self.close()
