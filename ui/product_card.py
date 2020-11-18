import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QFrame
from PyQt5.QtGui import QPixmap, QFont, QPainter, QPen
from PyQt5 import QtCore
import os


class ElementCard(QWidget):
    def __init__(self, title, cost, is_active):
        super().__init__()
        self.imagenumber = 0

        self.title = title
        self.cost = cost
        self.is_active = is_active

        self.initUI()
        self.label.setMouseTracking(True)
        self.frame_color = QtCore.Qt.darkGray

    def initUI(self):
        self.setStyleSheet('''
           QRadioButton::indicator {
               width:10px;
               height:10px;
               border: 1 px solid red;
               border-radius: 7px;
           }

           QRadioButton::indicator:checked {
               background-color:blue;
               border:2px solid blue;     
           }

           QRadioButton::indicator:unchecked {
               background-color:gray; 
               border: 2px solid gray; 
           }''')

        layout = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.setAlignment(QtCore.Qt.AlignHCenter)

        self.rb_group = QButtonGroup()
        self.radio0 = QRadioButton()
        self.radio1 = QRadioButton()
        self.radio2 = QRadioButton()
        self.radio3 = QRadioButton()

        self.radio0.setChecked(True)

        self.rb_group.addButton(self.radio0)
        self.rb_group.addButton(self.radio1)
        self.rb_group.addButton(self.radio2)
        self.rb_group.addButton(self.radio3)

        self.rb_group.setId(self.radio0, 0)
        self.rb_group.setId(self.radio1, 1)
        self.rb_group.setId(self.radio2, 2)
        self.rb_group.setId(self.radio3, 3)

        self.rb_group.buttonClicked.connect(self.rbPressEvent)

        hbox.addWidget(self.radio0)
        hbox.addWidget(self.radio1)
        hbox.addWidget(self.radio2)
        hbox.addWidget(self.radio3)

        self.name = QLabel(self.title)
        self.price = QLabel(self.cost)
        self.is_active = QLabel(self.is_active)

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
        self.label = QLabel()
        self.label.setMouseTracking(True)
        layout.addWidget(self.label)
        layout.addLayout(hbox)
        layout.addWidget(self.name)
        layout.addWidget(self.price)
        layout.addWidget(self.is_active)

        self.setFixedSize(300, 300)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showimage(0)
        # self.show()

    def showimage(self, imagenumber):
        directory = "C:/MyProgramms/1Main/Projects/Python/demoexam/Товары салона красоты"
        self.imagelist = os.listdir(directory)[:4]
        pixmap = QPixmap(directory + '\\' + self.imagelist[imagenumber])

        self.label.setPixmap(pixmap)
        # self.label.setFixedSize(200, 220)
        self.label.setScaledContents(True)

    def mouseMoveEvent(self, event):
        pos_x = event.pos().x()
        width = self.label.width()
        if pos_x <= width / 4:
            self.radio0.setChecked(True)
        elif pos_x >= width / 4 and pos_x <= width / 2:
            self.radio1.setChecked(True)
        elif pos_x >= width / 2 and pos_x <= width / 1.3:
            self.radio2.setChecked(True)
        else:
            self.radio3.setChecked(True)
        self.showimage(self.rb_group.checkedId())

    def rbPressEvent(self):
        self.showimage(self.rb_group.checkedId())

    # Цвет рамки заднего фона карточки

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.is_active.text() == 'Не активен':
            painter.setBrush(QtCore.Qt.gray)
        else:
            painter.setBrush(QtCore.Qt.white)
        painter.setPen(QPen(self.frame_color, 5))
        painter.drawRect(self.rect())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ElementCard('Антивозрастная коллекция Освежающий тоник Цветочный', '123', '342')
    ex.show()
    print(type(ElementCard))
    print(type(QWidget))
    sys.exit(app.exec_())