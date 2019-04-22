import sys
import os
from Window import Window
from pyqtgraph.Qt import QtGui, QtCore
import threading
from Dtw import check_gesture


def clear_data():
    folder = '../data'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def main():
    clear_data()
    app = QtGui.QApplication(sys.argv)
    win = Window(app)
    timer = QtCore.QTimer()
    timer.timeout.connect(win.serial_plot.update)
    timer.start(0)

    # thread = threading.Thread(
    #     target=check_gesture, args=(win.serial_plot.total_data,))
    # thread.daemon = True  # Daemonize thread
    # thread.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
