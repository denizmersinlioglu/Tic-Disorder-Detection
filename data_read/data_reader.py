import sys, serial, argparse
import numpy as np
from time import sleep
import re
from collections import deque
from hmmlearn import hmm

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# np.random.seed(42)
# model = hmm.GaussianHMM(n_components=3, covariance_type="full")
# model.startprob_ = np.array([0.6, 0.3, 0.1])
# model.transmat_ = np.array([[0.7, 0.2, 0.1], [0.3, 0.5, 0.2], [0.3, 0.3, 0.4]])
# model.means_ = np.array([[0.0, 0.0], [3.0, -3.0], [5.0, 10.0]])
# model.covars_ = np.tile(np.identity(2), (3, 1, 1))
# X, Z = model.sample(100)


class SerialPlot:
    # constr
    def __init__(self, strPort, maxLen):
        # open serial port
        self.ser = serial.Serial(port=strPort, baudrate=9600)

        self.accel_x = deque([0.0] * maxLen)
        self.accel_y = deque([0.0] * maxLen)
        self.accel_z = deque([0.0] * maxLen)
        self.gyro_x = deque([0.0] * maxLen)
        self.gyro_y = deque([0.0] * maxLen)
        self.gyro_z = deque([0.0] * maxLen)
        self.maxLen = maxLen

    # add to buffer
    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)

    # add data
    def add(self, data):
        assert (len(data) == 6)
        self.addToBuf(self.accel_x, data[0])
        self.addToBuf(self.accel_y, data[1])
        self.addToBuf(self.accel_z, data[2])
        self.addToBuf(self.gyro_x, data[3])
        self.addToBuf(self.gyro_y, data[4])
        self.addToBuf(self.gyro_z, data[5])

    # update plot
    def update(self, frameNum, a0, a1, a2, a3, a4, a5):
        try:
            line = self.ser.readline()
            data_str = re.findall(r"[-+]?\d*\.\d+|\d+", str(line))
            data = [float(val) for val in data_str]
            if (len(data) == 6):
                self.add(data)
                a0.set_data(range(self.maxLen), self.accel_x)
                a1.set_data(range(self.maxLen), self.accel_y)
                a2.set_data(range(self.maxLen), self.accel_z)
                a3.set_data(range(self.maxLen), self.gyro_x)
                a4.set_data(range(self.maxLen), self.gyro_y)
                a5.set_data(range(self.maxLen), self.gyro_z)
            else:
                print("Update doesn't used")
        except KeyboardInterrupt:
            print('exiting')

        return a0,

    # clean up
    def close(self):
        # close serial
        self.ser.flush()
        self.ser.close()


# main() function
def main():
    # create parser
    parser = argparse.ArgumentParser(description="LDR serial")
    # add expected arguments
    parser.add_argument('--port', dest='port', required=False)
    parser.add_argument('-l', dest='lenght', required=True)

    # parse args
    args = parser.parse_args()
    strPort = '/dev/cu.SLAB_USBtoUART'
    # strPort = args.port
    lenght = args.lenght
    print('reading from serial port %s...' % strPort)

    serialPlot = SerialPlot(strPort, int(lenght))
    COLOR = 'white'
    plt.rcParams['toolbar'] = 'None'
    plt.rcParams['text.color'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rcParams['xtick.color'] = COLOR
    plt.rcParams['ytick.color'] = COLOR

    print('Plotting data...')

    fig = plt.figure(figsize=(12, 6))
    fig.set_facecolor("black")
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
    ax.legend(loc='upper right')

    legend = plt.legend(frameon=1)
    frame = legend.get_frame()
    frame.set_facecolor('black')
    frame.set_edgecolor('white')

    _ = animation.FuncAnimation(
        fig, serialPlot.update, fargs=(a0, a1, a2, a3, a4, a5), interval=10)

    # show plot
    plt.show()
    # clean up
    serialPlot.close()
    print("Serial port closed safely")
    print('Exiting...')


# call main
if __name__ == '__main__':
    main()
