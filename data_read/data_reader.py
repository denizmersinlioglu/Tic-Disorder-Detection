import sys, argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
from SerialPort import SerialPlot
from hmmlearn import hmm
from pynput.keyboard import Key, Listener

# np.random.seed(42)
# model = hmm.GaussianHMM(n_components=3, covariance_type="full")
# model.startprob_ = np.array([0.6, 0.3, 0.1])
# model.transmat_ = np.array([[0.7, 0.2, 0.1], [0.3, 0.5, 0.2], [0.3, 0.3, 0.4]])
# model.means_ = np.array([[0.0, 0.0], [3.0, -3.0], [5.0, 10.0]])
# model.covars_ = np.tile(np.identity(2), (3, 1, 1))
# X, Z = model.sample(100)


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

    def key_press_event(event):
        print('you pressed', event.key, event.xdata, event.ydata)

    def key_release_event(event):
        print('you released', event.key, event.xdata, event.ydata)

    cid_press = fig.canvas.mpl_connect('key_press_event', key_press_event)
    cid_release = fig.canvas.mpl_connect('key_release_event',
                                         key_release_event)

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

    serialPlot = SerialPlot(strPort, 80)
    fig = configureFig()
    fargs = configureAx(80)
    print('Plotting data...')

    _ = animation.FuncAnimation(
        fig, serialPlot.update, fargs=fargs, interval=10)
    plt.show()

    serialPlot.close()
    print("Serial port closed safely")
    print('Exiting...')


# call main
if __name__ == '__main__':
    main()
