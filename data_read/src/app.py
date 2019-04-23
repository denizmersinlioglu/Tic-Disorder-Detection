import sys
import os
import serial
from pyqtgraph.Qt import QtGui, QtCore
import GRT
from Window import Window
from CustomThread import PredictionThread

STR_PORT = '/dev/cu.SLAB_USBtoUART'
BAUDRATE = 19200


def clear_data():
    '''
    Clears existing data of previous sessions from the hard disk. 
    Comment this method out to not loose data on every launch. 
    '''
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
    '''
    Executes the main application.
    Comment out clear data to keep previous session data.
    '''
    clear_data()
    # Create QTGui application
    app = QtGui.QApplication(sys.argv)

    # Open a serial port for serial plotter
    ser = serial.Serial(STR_PORT,
                        timeout=None,
                        baudrate=BAUDRATE,
                        xonxoff=False,
                        rtscts=False,
                        dsrdtr=False)
    ser.close()
    ser.open()
    print('Opening', ser.name)

    # Initialize a window for application GUI
    win = Window(app, ser)
    timer = QtCore.QTimer()
    timer.timeout.connect(win.serial_plot.update)
    timer.start(0)

    prediction_thread = PredictionThread()
    prediction_thread.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
