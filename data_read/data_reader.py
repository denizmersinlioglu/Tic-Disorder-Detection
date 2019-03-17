import sys, argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from SerialPlot import SerialPlot
from dtw import dtw

x = np.array([2, 0, 1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
y = np.array([1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
euclidean_norm = lambda x, y: np.abs(x - y)
d, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=euclidean_norm)
print(d)

x_lim = 250


def main():
    parser = argparse.ArgumentParser(description="LDR serial")
    parser.add_argument('--port', dest='port', required=False)
    # args = parser.parse_args()
    # strPort = args.port
    strPort = '/dev/cu.SLAB_USBtoUART'
    print('Reading from serial port %s...' % strPort)

    plot = SerialPlot(strPort, x_lim)
    print('Plotting data...')
    _ = animation.FuncAnimation(
        plot.fig, plot.port.update, fargs=plot.fargs, interval=1)

    plt.show()

    plot.port.close()
    print("Serial port closed safely")
    print('Exiting...')


# call main
if __name__ == '__main__':
    main()
