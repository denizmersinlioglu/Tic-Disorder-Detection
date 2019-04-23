from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import uuid
from Utils import *
from DTWGestureRecognizer import DTWGestureRecognizer
from CustomThread import ClassificationSampleThread


class RecordHelper:
    __instance = None

    @staticmethod
    def shared():
        ''' Static access method. '''
        if RecordHelper.__instance is None:
            RecordHelper()
        return RecordHelper.__instance

    def __init__(self):
        ''' Virtually private constructor. '''
        if RecordHelper.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.is_recording = False
            self.directory_holder = {x: [] for x in range(4)}
            self.recording_buffer = []
            self.directory = ""
            self.key = -1
            RecordHelper.__instance = self

    def begin_recording(self, key):
        ''' Start recording a gesture '''
        index = self.dir_params(key)
        if not self.is_recording:
            self.is_recording = True
            self.recording_buffer = []
        self.directory = "../data/{0}-{1}.csv".format(index, uuid.uuid4())
        self.key = index
        self.directory_holder[index].append(self.directory)

    def complete_recording(self, plotter):
        '''
        Complete recording a gesture.
        The gesture data will be cropped and be saved to desired directory. 
        '''
        if self.key != -1:
            cropped_gesture = crop_active_gesture(self.recording_buffer)
            sample = np.array(cropped_gesture)
            sample_thread = ClassificationSampleThread(self.key, sample)
            sample_thread.start()
            write_csv(cropped_gesture, self.directory)
            plotter.plot_data(cropped_gesture)

        else:
            sample = np.array(self.recording_buffer)
            sample_thread = ClassificationSampleThread(self.key, sample)
            sample_thread.start()
            write_csv(self.recording_buffer, self.directory)

        self.is_recording = False
        self.directory = ""
        self.key = -1
        self.recording_buffer = []

    def dir_params(self, key):
        '''
        Return directory values according to given key -> Pressed Key
        '''
        if key == QtCore.Qt.Key_1:
            return 0
        elif key == QtCore.Qt.Key_2:
            return 1
        elif key == QtCore.Qt.Key_3:
            return 2
        elif key == QtCore.Qt.Key_4:
            return 3
        elif key == QtCore.Qt.Key_Space:
            return -1
        else:
            raise ValueError('Unknow key pressed')
