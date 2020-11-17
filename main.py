import sys
import time

from PyQt5 import QtWidgets, QtGui, QtCore

from utils.app_style import ICO, WINDOW_STYLE_ID
from ui.product import ProductWindow

APP_NAME = 'Салон красоты'


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):
        # style
        self.setObjectName(WINDOW_STYLE_ID)
        style = open('theme/style.css', 'r')
        style = style.read()
        self.setStyleSheet(style)
        # product_btn
        self.product_btn = QtWidgets.QPushButton('Товары')
        self.product_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.product_btn.clicked.connect(self.click1)
        # quit_btn
        self.quit_btn = QtWidgets.QPushButton('Выйти')
        self.quit_btn.clicked.connect(app.quit)
        # logo
        self.logo = QtWidgets.QLabel()
        self.pixam = QtGui.QPixmap(ICO)
        self.logo.setPixmap(self.pixam)


        self.logo.setScaledContents(True)
        self.logo.setFixedSize(180, 180)
        # logo_wrapper
        self.logo_wrapper = QtWidgets.QHBoxLayout()
        self.logo_wrapper.addWidget(self.logo)
        # vbox
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.logo_wrapper)
        self.vbox.addWidget(self.product_btn)
        self.vbox.addWidget(self.quit_btn)
        # window
        self.setLayout(self.vbox)

        self.resize(500, 500)
        self.setMaximumSize(500, 500)
        self.setMinimumSize(500, 500)
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QtGui.QIcon(ICO))

        self.product_window = ProductWindow(self)

    def load_data(self, sp):
        for i in range(1, 11):
            time.sleep(0.2)
            sp.showMessage(f"Загрузка данных... {i * 10}%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom,
                           QtCore.Qt.black)

    def click1(self):
        self.product_window.show()


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
