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
#w.resize(1366,768)
wb = QtGui.QWidget(w)
win = pg.GraphicsWindow()

left_layout = QVBoxLayout()
saveButton = QPushButton('Save')
left_layout.addWidget(saveButton)
left_layout.addWidget(QPushButton('Bottom'))
wb.setLayout(left_layout)
layout = QHBoxLayout()
layout.addWidget(wb)
layout.addWidget(win)
# win.setFrameStyle(2)
w.setLayout(layout)


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
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
