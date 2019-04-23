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
        plot = self.addPlot()
        plot.setYRange(-30, 30, padding=0)
        plot.padding = 0
        plot0 = plot.plot(pen=pg.mkPen((255, 127, 14), width=2), name="AccelX")
        plot1 = plot.plot(pen=pg.mkPen((44, 160, 44), width=2), name="AccelY")
        plot2 = plot.plot(pen=pg.mkPen((31, 119, 180), width=2), name="AccelZ")
        plot3 = plot.plot(pen=pg.mkPen((148, 103, 189), width=2), name="GyroX")
        plot4 = plot.plot(pen=pg.mkPen((188, 189, 34), width=2), name="GyroY")
        plot5 = plot.plot(pen=pg.mkPen((140, 86, 75), width=2), name="GyroZ")
        self.plot = plot
        self.plots = [plot0, plot1, plot2, plot3, plot4, plot5]

    def plot_data(self, data):
        ''' Plot given data or data inside of a directory '''
        if isinstance(data, str):
            data = read_csv(data)

        if data is None or len(data[0]) != 6:
            return

        self.plot.setXRange(0, len(data), padding=0)
        for element in zip(self.plots, range(6)):
            (plot, offset) = element
            plot.setData([i[offset] for i in data])
