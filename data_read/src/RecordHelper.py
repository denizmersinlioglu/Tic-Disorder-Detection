from pyqtgraph.Qt import QtGui, QtCore
from Utils import *


class RecordHelper:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if RecordHelper.__instance is None:
            RecordHelper()
        return RecordHelper.__instance

    def __init__(self):
        """ Virtually private constructor. """

        if RecordHelper.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.recording_dir = [[], [], [], []]
            self.recording_count = [0, 0, 0, 0]
            self.is_recording = False
            self.recording_buffer = []
            self.active_directory = ""
            RecordHelper.__instance = self

    def begin_recording(self, key):
        (offset, element) = self.dir_params(key)
        if not self.is_recording:
            self.is_recording = True
            self.recording_buffer = []

        count = len(self.recording_dir[offset])
        directory = "../data/data{0}{1}.csv".format(element, count)
        if directory not in self.recording_dir[offset]:
            self.recording_dir[offset].append(directory)
            self.active_directory = directory

    def complete_recording(self, plotter):
        cropped_gesture = crop_active_gesture(self.recording_buffer)
        write_csv(cropped_gesture, self.active_directory)
        plotter.update_data(self.active_directory)
        self.is_recording = False
        self.active_directory = ""
        self.recording_buffer = []

    def dir_params(self, key):
        if key == QtCore.Qt.Key_1:
            return (0, key)
        elif key == QtCore.Qt.Key_2:
            return (1, key)
        elif key == QtCore.Qt.Key_3:
            return (2, key)
        elif key == QtCore.Qt.Key_4:
            return (3, key)
        else:
            raise ValueError('Unknow key pressed')
