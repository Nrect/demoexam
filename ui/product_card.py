import os

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QGridLayout, \
    QPushButton
from PyQt5.QtGui import QPixmap, QFont, QPainter, QPen
from PyQt5 import QtCore

from utils.app_style import RADIO_STYLE


class ElementCard(QWidget):
    def __init__(self, title, cost, main_image, product_photos, is_active):
        super().__init__()
        self.image_number = 0

        self.title = title
        self.cost = cost
        self.main_image = main_image
        self.product_photos = product_photos
        self.is_active = is_active

        self.frame_color = QtCore.Qt.gray

        self.init_ui()
        self.label.setMouseTracking(True)

    def init_ui(self):
        self.setStyleSheet(RADIO_STYLE)

        layout = QGridLayout()
        hbox = QHBoxLayout()
        hbox.setAlignment(QtCore.Qt.AlignHCenter)

        self.btn_edit = QPushButton('Изменить')
        self.btn_del = QPushButton('Удалить')

        self.label = QLabel()
        self.label.setMouseTracking(True)
        self.show_image(0)

        self.rb_group = QButtonGroup()
        self.radio_init(hbox)

        self.rb_group.button(0).setChecked(True)
        self.rb_group.buttonClicked.connect(self.rbPressEvent)

        hbox.addWidget(self.radio)

        self.name = QLabel(self.title)
        self.name.setWordWrap(True)
        self.price = QLabel(self.cost)
        self.price.setWordWrap(True)
        self.is_active = QLabel(self.is_active)
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

        self.setLayout(layout)
        layout.addWidget(self.label)
        layout.addLayout(hbox, 1, 0, alignment=QtCore.Qt.AlignHCenter)
        layout.addWidget(self.name)
        layout.addWidget(self.price)
        layout.addWidget(self.is_active)

        self.setFixedSize(300, 330)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    # TODO Доделать спавн картинок
    def show_image(self, imagenumber):
        directory = "./Товары салона красоты"
        self.imagelist = self.product_photos
        self.imagelist.insert(0, "./" + self.main_image)
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
        step = self.label.width() / len(self.imagelist)
        width_step = 0
        res = {}
        counter = 0
        while counter < len(self.imagelist):
            width_step += step
            res.update({counter: width_step})
            counter += 1
            for i in res.keys():
                if res[i] < x:
                    self.rb_group.button(i).setChecked(True)
        self.rbPressEvent()

    def contextMenuEvent(self, event):
        print(self.product_photos)

    # Цвет рамки заднего фона карточки
    def paintEvent(self, event):
        painter = QPainter(self)
        if self.is_active.text() == 'Не активен':
            painter.setBrush(QtCore.Qt.gray)
        else:
            painter.setBrush(QtCore.Qt.white)
        painter.setPen(QPen(self.frame_color, 5))
        painter.drawRect(self.rect())
