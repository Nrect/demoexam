from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QRadioButton, QButtonGroup, QGridLayout, QPushButton, \
    QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QPainter, QPen
from PyQt5 import QtCore

from ui.product_add_eddit import ProductForm

from utils.app_style import RADIO_STYLE
from utils.helpers import show_message, TYPES_FORM


class ElementCard(QWidget):
    def __init__(self, title, attached_products, cost, main_image, product_photos, is_active, description, uuid,
                 manufacturer
                 ):
        super().__init__()
        self.image_number = 0

        self.product_title = title
        self.product_attached_products = attached_products
        self.product_cost = cost
        self.product_main_image = main_image
        self.product_photos = product_photos
        self.product_is_active = is_active
        self.product_description = description
        self.product_uuid = uuid
        self.product_manufacturer = manufacturer

        self.frame_color = QtCore.Qt.gray

        self.init_ui()
        self.label.setMouseTracking(True)

    def init_ui(self):

        self.setStyleSheet(RADIO_STYLE)

        self.layout = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.setAlignment(QtCore.Qt.AlignHCenter)

        self.card_active_indicator = False

        # Кнопки
        self.btn_container = QHBoxLayout()

        self.btn_edit = QPushButton('Изменить')
        self.btn_edit.clicked.connect(self.btn_edit_click)

        self.btn_delete = QPushButton('Удалить')
        self.btn_delete.clicked.connect(self.btn_delete_click)

        self.btn_container.addWidget(self.btn_edit)
        self.btn_container.addWidget(self.btn_delete)

        self.btn_delete.hide()
        self.btn_edit.hide()

        # Изображение
        self.label = QLabel()
        self.label.setMouseTracking(True)
        self.show_image(0)

        # Радио-кнопки
        self.rb_group = QButtonGroup()
        self.radio_init(hbox)

        self.rb_group.button(0).setChecked(True)
        self.rb_group.buttonClicked.connect(self.rbPressEvent)

        hbox.addWidget(self.radio)

        self.name = QLabel(self.product_title + f"({self.product_attached_products})")
        self.name.setWordWrap(True)
        self.price = QLabel(self.product_cost)
        self.price.setWordWrap(True)
        self.is_active = QLabel(self.product_is_active)
        self.is_active.setWordWrap(True)

        self.name.setAlignment(QtCore.Qt.AlignHCenter)
        self.name.setMinimumWidth(100)
        self.name.setWordWrap(True)
        self.price.setAlignment(QtCore.Qt.AlignHCenter)
        self.name.setWordWrap(True)
        self.is_active.setAlignment(QtCore.Qt.AlignHCenter)
        self.name.setWordWrap(True)

        self.name.setFont(QFont('Roboto', 11, QFont.Normal))
        self.price.setFont(QFont('Roboto', 11, QFont.Normal))

        self.layout.addWidget(self.label)
        self.layout.addLayout(hbox)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.price)
        self.layout.addWidget(self.is_active)
        self.layout.addLayout(self.btn_container)

        self.setFixedSize(300, 330)
        self.setLayout(self.layout)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def show_image(self, imagenumber):
        self.imagelist = list(self.product_photos)
        self.imagelist.insert(0, "./" + self.product_main_image)
        pixmap = QPixmap(self.imagelist[imagenumber])
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

    def rbPressEvent(self):
        self.show_image(self.rb_group.checkedId())

    def radio_init(self, container):
        for i in range(len(self.imagelist)):
            self.radio = QRadioButton()
            self.rb_group.addButton(self.radio)
            self.rb_group.setId(self.radio, i)
            container.addWidget(self.radio)

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        step = self.label.width() / len(self.imagelist)
        width_step = 0
        res = {}
        counter = 0
        while counter < len(self.imagelist):
            width_step += step
            res.update({counter: width_step})
            counter += 1
            for i in res.keys():
                if y < self.label.height():
                    if res[i] < x:
                        self.rb_group.button(i).setChecked(True)
        self.rbPressEvent()

    def mousePressEvent(self, event):
        if not self.card_active_indicator:
            self.card_active_indicator = True
            self.btn_delete.show()
            self.btn_edit.show()
        else:
            self.card_active_indicator = False
            self.btn_delete.hide()
            self.btn_edit.hide()

    def btn_edit_click(self):
        try:
            self.product_form_window = ProductForm(TYPES_FORM[1], self.product_main_image, self.product_title,
                                                   self.product_cost, self.product_description, self.product_is_active,
                                                   self.product_uuid, self.product_manufacturer)
        except Exception as e:
            print(e)
        self.product_form_window.show()

    # TODO Сделать удаление товара по заданию
    def btn_delete_click(self):
        try:
            show_message('Удалить товар?', '', self.btn_message_click)
        except Exception as e:
            print(e)

    # TODO Сделать удаление товара по заданию
    def btn_message_click(self, i):
        print(i.text())

    # Цвет рамки заднего фона карточки
    def paintEvent(self, event):
        painter = QPainter(self)
        if self.is_active.text() == 'Не активен':
            painter.setBrush(QtCore.Qt.gray)
        else:
            painter.setBrush(QtCore.Qt.white)
        painter.setPen(QPen(self.frame_color, 5))
        painter.drawRect(self.rect())
