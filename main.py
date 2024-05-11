import sys

from PyQt5 import QtWidgets
from mainwindow import MainWindow

app = QtWidgets.QApplication(sys.argv)
mw = MainWindow()
mw.show()
sys.exit(app.exec())