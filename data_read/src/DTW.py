from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import numpy as np
import csv


class DTW:
    def __init__(self):
        self.key = 0
        self.main_directory = "../data"

    def calculate_gradient(self, data):
        return np.gradient(np.array(data, dtype=float), axis=0)

    def read_csv(self, directory):
        result = []
        with open(directory, 'r') as infile:
            reader = csv.reader(infile, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:  # each row is a list
                result.append(row)
        return result

    def dtw_distance(self, x, directory):
        reading = self.read_csv(directory)
        y = np.array(reading)
        distance, path = fastdtw(x, y, dist=euclidean)
        return distance
