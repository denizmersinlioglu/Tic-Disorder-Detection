import sys
from PyQt5 import QtGui


class Window(QtGui.QMainWidow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle()
