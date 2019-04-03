from fastdtw import fastdtw
import numpy as np
import csv
from scipy import signal


class DTW:
    def __init__(self):
        self.key = 0
        self.main_directory = "../data"
        self.smooth_window_size = 5
        self.smooth_polynomial = 1

    def smooth_data(self, data):
        smoothed = []
        if len(data[0]) > 0:
            for i in range(0, len(data[0])):
                coloumn = np.array(data)[:, i]
                smoothed_coloumn = signal.savgol_filter(
                    coloumn, self.smooth_window_size, self.smooth_polynomial)
                if i == 0:
                    smoothed = smoothed_coloumn
                else:
                    smoothed = np.c_[smoothed, smoothed_coloumn]
        return smoothed

    def calculate_gradient(self, data):
        return np.gradient(np.array(data, dtype=float), axis=0)

    def read_csv(self, directory):
        result = []
        with open(directory, 'r') as infile:
            reader = csv.reader(infile, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:  # each row is a list
                result.append(row)
        return result

    def dtw_distance(self, live_data, directory):
        recorded_data = self.read_csv(directory)
        np_recorded_data = np.array(recorded_data)

        if live_data == None:
            return None

        if len(live_data) > 10:
            distance, _ = fastdtw(live_data, np_recorded_data)
            return distance
        else:
            return None
