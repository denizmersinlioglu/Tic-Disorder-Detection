import pyqtgraph as pg
import numpy as np
from collections import deque
from RecordHelper import RecordHelper
from DTWGestureRecognizer import DTWGestureRecognizer
import concurrent.futures


class SerialPlot(pg.GraphicsWindow):
    def __init__(self, app, max_len, serial):
        super(SerialPlot, self).__init__()
        self.resize(1200, 450)
        self.app = app
        self.max_len = max_len
        self.serial = serial

        plot = self.addPlot()
        plot.setYRange(-30, 30, padding=0)
        plot.setXRange(0, max_len, padding=0)
        plot.addLegend()
        plot0 = plot.plot(pen=pg.mkPen((255, 127, 14), width=3), name="AccelX")
        plot1 = plot.plot(pen=pg.mkPen((44, 160, 44), width=3), name="AccelY")
        plot2 = plot.plot(pen=pg.mkPen((31, 119, 180), width=3), name="AccelZ")
        plot3 = plot.plot(pen=pg.mkPen((148, 103, 189), width=3), name="GyroX")
        plot4 = plot.plot(pen=pg.mkPen((188, 189, 34), width=3), name="GyroY")
        plot5 = plot.plot(pen=pg.mkPen((140, 86, 75), width=3), name="GyroZ")

        self.plots = [plot0, plot1, plot2, plot3, plot4, plot5]
        self.current_data = [deque([0.0] * max_len) for _ in range(6)]

    def addToBuf(self, buf, val):
        if len(buf) < self.max_len:
            buf.append(val)
        else:
            buf.popleft()
            buf.append(val)

    def update(self):
        '''
        Read the serial data and plot it
        Recording handled by Record Helper 
        '''
        if not self.serial.in_waiting:
            self.app.processEvents()
            return
        try:
            line = str(self.serial.readline(), 'utf-8').split("\t")
            data = [float(i) for i in line]

            if RecordHelper.shared().is_recording:
                RecordHelper.shared().recording_buffer.append(data)
                DTWGestureRecognizer.shared().active_data = None
            else:
                DTWGestureRecognizer.shared().active_data = data

            for element in zip(self.current_data, data, self.plots):
                (buffer, datum, plot) = element
                self.addToBuf(buffer, datum)
                plot.setData(buffer)

            self.app.processEvents()

        except Exception as ex:
            print(ex)
