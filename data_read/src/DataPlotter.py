import pyqtgraph as pg
from Utils import read_csv


class DataPlotter(pg.GraphicsWindow):
    '''
    Plots data in order to visualize the gestures and real-time captured data.
    It is a subclass of pg.GraphicsWindow and contains a plot init.
    '''

    def __init__(self):
        super(DataPlotter, self).__init__()
        self.resize(400, 300)
        self.plot = self.addPlot()
        self.plot.padding = 0
        self.plot.setYRange(-30, 30, padding=0)
        self.plot0 = self.plot.plot(pen=pg.mkPen((255, 127, 14), width=1),
                                    name="Accel_X")
        self.plot1 = self.plot.plot(pen=pg.mkPen((44, 160, 44), width=1),
                                    name="Accel_Y")
        self.plot2 = self.plot.plot(pen=pg.mkPen((31, 119, 180), width=1),
                                    name="Accel_Z")
        self.plot3 = self.plot.plot(pen=pg.mkPen((148, 103, 189), width=1),
                                    name="Gyro_X")
        self.plot4 = self.plot.plot(pen=pg.mkPen((188, 189, 34), width=1),
                                    name="Gyro_Y")
        self.plot5 = self.plot.plot(pen=pg.mkPen((140, 86, 75), width=1),
                                    name="Gyro_Z")

    def update_data(self, data):
        if isinstance(data, str):
            data = read_csv(data)

        if data == None or len(data[0]) != 6:
            return
        self.plot.setXRange(0, len(data), padding=0)
        self.plot0.setData([i[0] for i in data])
        self.plot1.setData([i[1] for i in data])
        self.plot2.setData([i[2] for i in data])
        self.plot3.setData([i[3] for i in data])
        self.plot4.setData([i[4] for i in data])
        self.plot5.setData([i[5] for i in data])
