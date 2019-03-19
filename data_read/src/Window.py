import csv
import threading

from DTW import DTW
from SerialPlot import SerialPlot
from DataPlotter import DataPlotter
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
import numpy as np
strPort = '/dev/cu.SLAB_USBtoUART'
baudRate = 19200


class Window(QtGui.QWidget):
    def __init__(self, app):
        super(Window, self).__init__()
        self.setWindowTitle('Tic Disorder Detection')
        self.main_layout = QVBoxLayout()
        self.record_dir = [[], [], [], []]
        self.record_count = [0, 0, 0, 0]
        self.wb = QtGui.QWidget(self)
        self.button_layout = QVBoxLayout()
        self.saveButton = QPushButton('Calculate Distance')
        self.saveButton.setFixedHeight(50)
        self.button_layout.addWidget(self.saveButton)
        # button_layout.addWidget(QPushButton('Bottom'))
        self.wb.setLayout(self.button_layout)

        self.wsg_container = QtGui.QWidget(self)
        self.wsg_container_layout = QHBoxLayout()
        self.wsg_container.setLayout(self.wsg_container_layout)

        self.serial_plot = SerialPlot(strPort, baudRate, app, 127)

        self.main_layout.addWidget(self.serial_plot)
        self.main_layout.addWidget(self.wb)
        self.main_layout.addWidget(self.wsg_container)
        self.setLayout(self.main_layout)

        self.saveButton.clicked.connect(self.on_click)
        self.first_gesture = DataPlotter()
        self.wsg_container_layout.addWidget(self.first_gesture)
        self.second_gesture = DataPlotter()
        self.wsg_container_layout.addWidget(self.second_gesture)
        self.third_gesture = DataPlotter()
        self.wsg_container_layout.addWidget(self.third_gesture)
        self.fourth_gesture = DataPlotter()
        self.wsg_container_layout.addWidget(self.fourth_gesture)
        self.show()

    def get_dir_params(self, key):
        if key == QtCore.Qt.Key_1:
            return (0, key, self.first_gesture)
        elif key == QtCore.Qt.Key_2:
            return (1, key, self.second_gesture)
        elif key == QtCore.Qt.Key_3:
            return (2, key, self.third_gesture)
        elif key == QtCore.Qt.Key_4:
            return (3, key, self.fourth_gesture)
        else:
            raise ValueError('Unknow key pressed')

    def keyPressEvent(self, event):
        try:
            (offset, element, _) = self.get_dir_params(event.key())
            if not self.serial_plot.is_recording:
                self.serial_plot.is_recording = True
                self.serial_plot.record_buffer = []
                count = len(self.record_dir[offset])
                _dir = "../data/data{0}{1}.csv".format(element, count)
                if _dir not in self.record_dir[offset]:
                    self.record_dir[offset].append(_dir)
                    self.serial_plot.directory = _dir
        except Exception as e:
            print(e)

    def keyReleaseEvent(self, event):
        try:
            (offset, _, plotter) = self.get_dir_params(event.key())
            self.serial_plot.is_recording = False
            self.serial_plot.write_csv()
            _dir = self.record_dir[offset][-1]
            plotter.plot_data_from(_dir)
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_click(self):
        self.serial_plot.calculate_dtw(self.fourth_gesture)
        # thread = threading.Thread(
        #     target=, args=)
        # thread.daemon = True  # Daemonize thread
        # thread.start()
        print('PyQt5 button click')
