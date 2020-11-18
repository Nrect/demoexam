import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QSplashScreen
from PyQt5.QtGui import QPixmap, QCursor, QIcon

from ui.product import ProductWindow

from utils.app_style import ICO
from utils.consts import APP_NAME
from utils.helpers import set_window_style, load_data


class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        set_window_style(self)
        self.product_window = ProductWindow(self)
        self.init_ui()

    def init_ui(self):
        # product_btn
        product_btn = QPushButton('Товары')
        product_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        product_btn.clicked.connect(self.show_product_window)
        # quit_btn
        quit_btn = QPushButton('Выйти')
        quit_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        quit_btn.clicked.connect(app.quit)
        # Логотип
        logo = QLabel()
        pixam = QPixmap(ICO)
        logo.setPixmap(pixam)
        logo.setScaledContents(True)
        logo.setFixedSize(180, 180)
        # Обертка лого
        logo_wrapper = QHBoxLayout()
        logo_wrapper.addWidget(logo)
        # Контейнер
        vbox = QVBoxLayout()
        vbox.addLayout(logo_wrapper)
        vbox.addWidget(product_btn)
        vbox.addWidget(quit_btn)
        # Окно
        self.setLayout(vbox)
        self.resize(500, 500)
        self.setMaximumSize(500, 500)
        self.setMinimumSize(500, 500)
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(ICO))

    def show_product_window(self):
        self.product_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    # Окно загрузки
    splash = QSplashScreen(QPixmap("beauty_logo.ico"))
    splash.showMessage("Загрузка данных... 0%",
                       QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    splash.show()
    load_data(splash)
    splash.finish(main)

    main.show()
    sys.exit(app.exec_())
