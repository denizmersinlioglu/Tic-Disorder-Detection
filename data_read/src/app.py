import sys
import os
import serial
from pyqtgraph.Qt import QtGui, QtCore
import GRT
from Window import Window

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


def dtw_pipeline():
    '''
    Returns a pipeline object in order to detect real time gestures by several methods.
    '''
    pipeline = GRT.GestureRecognitionPipeline()
    classifier = GRT.DTW()

    # Turn on null rejection, this lets the classifier output the predicted class
    # label of 0 when the likelihood of a gesture is low
    classifier.enableNullRejection = True

    # Set the null rejection coefficient to 3, this controls
    # the thresholds for the automatic null rejection
    # You can increase this value if you find that your
    # real-time gestures are not being recognized
    # If you are getting too many false positives then you should decrease this value
    classifier.setNullRejectionCoeff(3)

    # Turn on the automatic data triming, this will remove
    # any sections of none movement from the start and end of the training samples
    classifier.enableTrimTrainingData(True, 0.1, 90)

    # Offset the timeseries data by the first sample,
    # this makes your gestures (more) invariant to the location the gesture is performed
    classifier.setOffsetTimeseriesUsingFirstSample(True)

    # Allow the DTW algorithm to search the entire cost matrix
    classifier.setContrainWarpingPath(True)

    pipeline.setClassifier(classifier)
    pipeline.classificationData = GRT.TimeSeriesClassificationData()
    pipeline.trainingData = GRT.TimeSeriesClassificationData()
    pipeline.classificationData.setNumDimensions(6)

    return pipeline


def main():
    '''
    Executes the main application.
    Comment out clear data to keep previous session data.
    '''
    clear_data()
    # Create QTGui application
    app = QtGui.QApplication(sys.argv)

    # Open a serial port for serial plotter
    ser = serial.Serial(STR_PORT, BAUDRATE, timeout=1)
    ser.close()
    ser.open()
    print('Opening', ser.name)

    # Initialize a window for application GUI
    win = Window(app, ser)
    timer = QtCore.QTimer()
    timer.timeout.connect(win.serial_plot.update)
    timer.start(0)

    # pipeline = dtw_pipeline()
    # vector = np.array([1, 2, 3, 1.2, 2.3, 3.4])
    # matrix = np.array([[1.2, 2.3, 3.4, 1.2, 2.3, 3.4],
    #                    [3.3, 3.2, 5.5, 1.2, 2.3, 3.4]])
    # appended = np.vstack([matrix, vector])
    # pipeline.classificationData.addSample(0, appended)

    # thread = threading.Thread(
    #     target=check_gesture, args=(win.serial_plot.total_data,))
    # thread.daemon = True  # Daemonize thread
    # thread.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
