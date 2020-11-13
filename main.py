import sys
import time

from PyQt5 import QtWidgets, QtGui, QtCore

from utils.app_style import ICO, MAIN_STYLE, WINDOW_STYLE_ID
from ui.manufacture import ManufactureWindow
from ui.window2 import Window2

APP_NAME = 'Салон красоты'


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # product btn
        self.product_btn = QtWidgets.QPushButton('Товары')
        self.product_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.product_btn.clicked.connect(self.click1)
        # logo
        self.logo = QtWidgets.QLabel()
        self.pixam = QtGui.QPixmap(ICO)
        self.logo.setPixmap(self.pixam)

        self.logo.setAlignment(QtCore.Qt.AlignRight)
        self.logo.setScaledContents(True)
        self.logo.setFixedSize(180,180)
        # logo_wrapper
        self.logo_wrapper = QtWidgets.QHBoxLayout()
        self.logo_wrapper.addWidget(self.logo)
        # vbox
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.logo_wrapper)
        self.vbox.addWidget(self.product_btn)
        # window
        self.setObjectName(WINDOW_STYLE_ID)
        self.setStyleSheet(MAIN_STYLE)
        self.setLayout(self.vbox)

        self.resize(500, 500)
        self.setMaximumSize(500, 500)
        self.setMinimumSize(500, 500)
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QtGui.QIcon(ICO))


        # self.new_window = Window2(self)
        self.manufacture_window = ManufactureWindow(self)
    def load_data(self, sp):
        for i in range(1, 11):
            time.sleep(0.2)
            sp.showMessage(f"Загрузка данных... {i * 10}%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom,
                           QtCore.Qt.black)

    def click1(self):
        self.manufacture_window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("beauty_logo.ico"))
    splash.showMessage("Загрузка данных... 0%",
                       QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    splash.show()  # Отображаем заставку

    main = MainWindow()
    main.load_data(splash)
    main.show()
    splash.finish(main)

    sys.exit(app.exec_())
