import csv
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


class DataPlotter(pg.GraphicsWindow):
    def __init__(self):
        super(DataPlotter, self).__init__()
        self.resize(400, 300)
        self.plotter = self.addPlot()
        self.plotter.padding = 0
        self.plotter.setYRange(-30, 30, padding=0)
        self.plot0 = self.plotter.plot(
            pen=pg.mkPen((255, 127, 14), width=1), name="Accel_X")
        self.plot1 = self.plotter.plot(
            pen=pg.mkPen((44, 160, 44), width=1), name="Accel_Y")
        self.plot2 = self.plotter.plot(
            pen=pg.mkPen((31, 119, 180), width=1), name="Accel_Z")
        self.plot3 = self.plotter.plot(
            pen=pg.mkPen((148, 103, 189), width=1), name="Gyro_X")
        self.plot4 = self.plotter.plot(
            pen=pg.mkPen((188, 189, 34), width=1), name="Gyro_Y")
        self.plot5 = self.plotter.plot(
            pen=pg.mkPen((140, 86, 75), width=1), name="Gyro_Z")

    def read_csv(self, directory):
        result = []
        with open(directory, 'r') as infile:
            reader = csv.reader(infile, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:  # each row is a list
                result.append(row)
        return result

    def plot_data_from(self, directory):
        result = self.read_csv(directory)
        self.update_data(result)

    def update_data(self, data):
        if data == None or len(data[0]) != 6:
            return
        self.plotter.setXRange(0, len(data), padding=0)
        self.plot0.setData([i[0] for i in data])
        self.plot1.setData([i[1] for i in data])
        self.plot2.setData([i[2] for i in data])
        self.plot3.setData([i[3] for i in data])
        self.plot4.setData([i[4] for i in data])
        self.plot5.setData([i[5] for i in data])
