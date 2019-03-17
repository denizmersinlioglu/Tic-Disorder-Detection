from SerialPort import SerialPort
import matplotlib.pyplot as plt


class SerialPlot:
    def __init__(self, port, lenght):

        self.fig = self.configureFig()
        self.port = SerialPort(port, lenght, self.fig)
        self.fargs = self.configureAx(lenght)

    def configureFig(self):
        COLOR = 'white'
        plt.rcParams['toolbar'] = 'None'
        plt.rcParams['text.color'] = COLOR
        plt.rcParams['axes.labelcolor'] = COLOR
        plt.rcParams['axes.labelcolor'] = COLOR
        plt.rcParams['xtick.color'] = COLOR
        plt.rcParams['ytick.color'] = COLOR
        fig = plt.figure(figsize=(6, 6))
        fig.set_facecolor("black")

        return fig

    def configureAx(self, lenght):
        ax = plt.axes(xlim=(0, int(lenght)), ylim=(-30, 30))
        ax.set_facecolor('black')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.yaxis.grid(color='#222222', linestyle='dashed')
        ax.xaxis.grid(color='#222222', linestyle='dashed')
        a0, = ax.plot([], [], label='Acc_X')
        a1, = ax.plot([], [], label='Acc_Y')
        a2, = ax.plot([], [], label='Acc_Z')
        a3, = ax.plot([], [], label='Gyro_X')
        a4, = ax.plot([], [], label='Gyro_Y')
        a5, = ax.plot([], [], label='Gyro_Z')
        ax.legend(loc='upper left')
        ax.legend(ncol=6)
        legend = plt.legend(frameon=1)
        frame = legend.get_frame()
        frame.set_facecolor('black')
        frame.set_edgecolor('white')
        return (a0, a1, a2, a3, a4, a5)
