import sys, argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from SerialPlot import SerialPlot
from pyqtgraph.ptime import time
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSlot
from dtw import dtw
import pyqtgraph as pg
# x = np.array([2, 0, 1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
# y = np.array([1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
# euclidean_norm = lambda x, y: np.abs(x - y)
# d, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=euclidean_norm)
# print(d)

app = QtGui.QApplication([])

## Define a top-level widget to hold everything
w = QtGui.QWidget()
w.setWindowTitle('MPU9250 features acquisition')
main_layout = QVBoxLayout()

#w.resize(1366,768)
wb = QtGui.QWidget(w)
button_layout = QVBoxLayout()
saveButton = QPushButton('Save')
saveButton.setFixedHeight(50)
button_layout.addWidget(saveButton)
# button_layout.addWidget(QPushButton('Bottom'))
wb.setLayout(button_layout)

wsg_container = QtGui.QWidget(w)
wsg_container_layout = QHBoxLayout()

# Windows of Saved Graph
wsg1 = pg.GraphicsWindow()
wsg1.resize(100, 200)
wsg_container_layout.addWidget(wsg1)
wsg2 = pg.GraphicsWindow()
wsg2.resize(100, 200)
wsg_container_layout.addWidget(wsg2)
wsg3 = pg.GraphicsWindow()
wsg3.resize(100, 200)
wsg_container_layout.addWidget(wsg3)
wsg_container.setLayout(wsg_container_layout)

win = pg.GraphicsWindow()
win.resize(1000, 400)

main_layout.addWidget(win)
main_layout.addWidget(wb)
main_layout.addWidget(wsg_container)

# win.setFrameStyle(2)
w.setLayout(main_layout)


@pyqtSlot()
def on_click():
    print('PyQt5 button click')


saveButton.clicked.connect(on_click)

p_main = win.addPlot()

strPort = '/dev/cu.SLAB_USBtoUART'
baudRate = 19200
p_main.setMenuEnabled(False)
serial_plot = SerialPlot(strPort, baudRate, app, p_main, 127)

w.show()

timer = QtCore.QTimer()
timer.timeout.connect(serial_plot.update)
timer.start(0)

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
