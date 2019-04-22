import pyqtgraph as pg
import serial
from collections import deque
import csv
import pyqtgraph as pg
import numpy as np
from scipy import signal
import time
from Dtw import smooth_data


class SerialPlot(pg.GraphicsWindow):
    def __init__(self, port, baudRate, app, maxLen, gesture_plotter):
        super(SerialPlot, self).__init__()
        self.resize(1200, 400)
        self.gesture_plotter = gesture_plotter
        self.app = app
        self.maxLen = maxLen
        self.bytecount = 300  # This variable sets the number of bytes to read in
        self.cnt = 0
        self.is_recording = False
        self.directory = ""
        self.p = self.addPlot()
        self.p.setYRange(-30, 30, padding=0)
        self.p.setXRange(0, maxLen, padding=0)
        # self.p.setInteractive(False)
        self.p.addLegend()
        self.plot0 = self.p.plot(
            pen=pg.mkPen((255, 127, 14), width=3), name="Accel_X")
        self.plot1 = self.p.plot(
            pen=pg.mkPen((44, 160, 44), width=3), name="Accel_Y")
        self.plot2 = self.p.plot(
            pen=pg.mkPen((31, 119, 180), width=3), name="Accel_Z")
        self.plot3 = self.p.plot(
            pen=pg.mkPen((148, 103, 189), width=3), name="Gyro_X")
        self.plot4 = self.p.plot(
            pen=pg.mkPen((188, 189, 34), width=3), name="Gyro_Y")
        self.plot5 = self.p.plot(
            pen=pg.mkPen((140, 86, 75), width=3), name="Gyro_Z")
        self.data0 = deque([0.0] * maxLen)
        self.data1 = deque([0.0] * maxLen)
        self.data2 = deque([0.0] * maxLen)
        self.data3 = deque([0.0] * maxLen)
        self.data4 = deque([0.0] * maxLen)
        self.data5 = deque([0.0] * maxLen)
        self.total_data = deque([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]] * maxLen)

        self.ser = serial.Serial(port, baudRate, timeout=1)
        self.ser.close()
        self.ser.open()
        self.record_buffer = []
        print('Opening', self.ser.name)
        print('Reading Serial port =', self.bytecount, 'bytes')

    def write_csv(self):
        smoothed = smooth_data(self.record_buffer)
        gradient = np.gradient(np.array(smoothed, dtype=float), axis=0)
        norm = ([np.linalg.norm(i) for i in gradient])
        first_index = next(x[0] for x in enumerate(norm) if x[1] >= 1)
        last_index = len(norm) - next(
            x[0] for x in enumerate(reversed(norm)) if x[1] >= 1)
        recording_data = self.record_buffer[first_index:last_index]
        with open(self.directory, 'w') as outfile:
            writer = csv.writer(outfile)
            for row in recording_data:
                writer.writerow(row)

    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.popleft()
            buf.append(val)

    def update(self):
        try:
            line = str(self.ser.readline(), 'utf-8').split("\t")
            data = [float(i) for i in line]

            if self.is_recording:
                self.record_buffer.append(data)

            self.addToBuf(self.total_data, data)
            self.addToBuf(self.data0, data[0])
            self.addToBuf(self.data1, data[1])
            self.addToBuf(self.data2, data[2])
            self.addToBuf(self.data3, data[3])
            self.addToBuf(self.data4, data[4])
            self.addToBuf(self.data5, data[5])

            self.plot0.setData(self.data0)
            self.plot1.setData(self.data1)
            self.plot2.setData(self.data2)
            self.plot3.setData(self.data3)
            self.plot4.setData(self.data4)
            self.plot5.setData(self.data5)
            self.app.processEvents()

        except Exception as e:
            print(e)
