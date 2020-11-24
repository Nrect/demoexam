import sys
from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel, QComboBox, QVBoxLayout, QApplication, QCheckBox, \
    QHBoxLayout, QPushButton

from utils.helpers import set_window_style


class ProductForm(QWidget):
    def __init__(self):
        super().__init__()
        # set_window_style(self)
        self.init_ui()

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
        # Данные товара
        self.product_uuid = QLineEdit()
        self.product_name = QLineEdit()
        self.product_cost = QLineEdit()
        self.product_description = QLineEdit()
        self.product_main_photo = QLabel()
        self.product_manufacturer = QComboBox()

        self.product_is_active = QCheckBox()
        self.product_is_active.setChecked(True)

        # Добавление элементов
        form_layout.addRow(QLabel('Фото:'), self.product_main_photo)
        form_layout.addRow(QLabel('Идентификатор:'), self.product_uuid)
        form_layout.addRow(QLabel('Наименование:'), self.product_name)
        form_layout.addRow(QLabel('Стоимость:'), self.product_cost)
        form_layout.addRow(QLabel('Описание:'), self.product_description)
        form_layout.addRow(QLabel('Производитель:'), self.product_manufacturer)
        form_layout.addRow(QLabel('Активен?'), self.product_is_active)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)
        # Окно
        self.setLayout(main_layout)

    def show_window(self):
        self.show()


if __name__ == '__main__':
    import sys

    qapp = QApplication(sys.argv)
    pd = ProductForm()
    pd.show()
    sys.exit(qapp.exec_())
