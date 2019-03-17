import sys, argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from SerialPort import SerialPlot
from pynput.keyboard import Key, Listener
from dtw import dtw

x = np.array([2, 0, 1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
y = np.array([1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)

euclidean_norm = lambda x, y: np.abs(x - y)

d, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=euclidean_norm)
print(d)


def configureFig():
    COLOR = 'white'
    plt.rcParams['toolbar'] = 'None'
    plt.rcParams['text.color'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rcParams['xtick.color'] = COLOR
    plt.rcParams['ytick.color'] = COLOR
    fig = plt.figure(figsize=(12, 6))
    fig.set_facecolor("black")

    return fig


def configureAx(lenght):
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
    return (a0, a1, a2, a3, a4, a5)


def main():
    parser = argparse.ArgumentParser(description="LDR serial")
    parser.add_argument('--port', dest='port', required=False)
    # args = parser.parse_args()
    # strPort = args.port
    strPort = '/dev/cu.SLAB_USBtoUART'
    print('Reading from serial port %s...' % strPort)

    fig = configureFig()
    plot = SerialPlot(strPort, 80, fig)

    fargs = configureAx(80)
    print('Plotting data...')

    _ = animation.FuncAnimation(fig, plot.update, fargs=fargs, interval=1)

    plt.show()

    plot.close()
    print("Serial port closed safely")
    print('Exiting...')


# call main
if __name__ == '__main__':
    main()
