from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSlot
from pyqtgraph.Qt import QtGui, QtCore
from SerialPlot import SerialPlot
from DataPlotter import DataPlotter
from RecordHelper import RecordHelper


class Window(QtGui.QWidget):
    def __init__(self, app, serial):
        super(Window, self).__init__()
        self.setWindowTitle('Tic Disorder Detection')
        self.main_layout = QVBoxLayout()
        self.window = QtGui.QWidget(self)
        self.button_layout = QVBoxLayout()
        self.window.setLayout(self.button_layout)

        self.gesture_layout = QHBoxLayout()
        self.gesture_container = QtGui.QWidget(self)
        self.gesture_container.setLayout(self.gesture_layout)

        self.data_plotters = [DataPlotter() for _ in range(4)]
        for plotter in self.data_plotters:
            self.gesture_layout.addWidget(plotter)

        self.serial_plot = SerialPlot(app, 127, serial)
        self.main_layout.addWidget(self.serial_plot)
        self.main_layout.addWidget(self.window)
        self.main_layout.addWidget(self.gesture_container)

        self.setLayout(self.main_layout)
        self.show()

    def keyPressEvent(self, event):
        ''' Key Press Event for training Gesture '''
        try:
            key = event.key()
            if not RecordHelper.shared().is_recording:
                RecordHelper.shared().begin_recording(key)
        except Exception as exception:
            print(exception)

    def keyReleaseEvent(self, event):
        ''' Key Release Event for training Gesture '''
        try:
            key = event.key()
            index = RecordHelper.shared().dir_params(key)
            active_plotter = self.data_plotters[index]
            RecordHelper.shared().complete_recording(active_plotter)
        except Exception as exception:
            print(exception)
