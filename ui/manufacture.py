from PyQt5 import QtCore, QtWidgets, QtSql, QtGui
from utils.consts import TABLE_PRODUCT
from utils.connection_string import connection_string
from utils.app_style import ICO
import sys


class ManufactureWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ManufactureWindow, self).__init__(parent,QtCore.Qt.Window)
        self.initUI()

    def initUI(self):
        self.table_widget = QtWidgets.QTableView()
        self.connection_string = connection_string.create_connection()

        self.sqm = QtSql.QSqlQueryModel()
        self.sqm.setQuery(f'select * from {TABLE_PRODUCT}')

        self.sqm.setHeaderData(0, QtCore.Qt.Horizontal, 'Название')
        self.sqm.setHeaderData(1, QtCore.Qt.Horizontal, 'Цена')
        self.sqm.setHeaderData(2, QtCore.Qt.Horizontal, 'Описание')
        self.sqm.setHeaderData(3, QtCore.Qt.Horizontal, 'Изображение')
        self.sqm.setHeaderData(4, QtCore.Qt.Horizontal, 'Активен')
        self.sqm.setHeaderData(5, QtCore.Qt.Horizontal, 'Производитель')



        self.table_widget.setModel(self.sqm)
        self.table_widget.setColumnWidth(1, 150)
        self.table_widget.setColumnWidth(2, 60)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.table_widget)

        self.setLayout(self.vbox)
        self.setWindowModality(2)
        self.setWindowIcon(QtGui.QIcon(ICO))
        self.setWindowTitle('Производитель')
        self.resize(1500, 900)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = ManufactureWindow()
    main.show()
    sys.exit(app.exec_())
