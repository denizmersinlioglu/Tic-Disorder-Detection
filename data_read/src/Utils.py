import csv
import numpy as np
from scipy import signal

MAIN_DIRECTORY = "../data"
SMOOTH_WINDOW_SIZE = 5
SMOOTH_POLYNOMIAL = 1


def read_csv(directory):
    '''
    Reads data from given directory and writes into an array.
    Returns array of data inside the directory
    '''
    result = []
    with open(directory, 'r') as infile:
        reader = csv.reader(infile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:  # each row is a list
            result.append(row)
    return result


def write_csv(data, directory):
    '''
    Writes the data to given directory.
    '''
    with open(directory, 'w') as outfile:
        writer = csv.writer(outfile)
        for row in data:
            writer.writerow(row)


def smooth_data(data):
    '''
    Smooth data in order to prevent noise.
    Smoothing is needed to crop data with respect to its gradient peaks.
    '''
    smoothed = []
    row_lenght = len(data[0])
    if row_lenght > 0:
        for i in range(0, row_lenght):
            coloumn = np.array(data)[:, i]
            smoothed_coloumn = signal.savgol_filter(coloumn,
                                                    SMOOTH_WINDOW_SIZE,
                                                    SMOOTH_POLYNOMIAL)
            if i == 0:
                smoothed = smoothed_coloumn
            else:
                smoothed = np.c_[smoothed, smoothed_coloumn]
    return smoothed


def crop_active_gesture(data):
    '''
    Crops the inactive tail and header areas from input data.
    Calculates the gradient of the data and cuts from first peak,
    also cuts after last peak of the gradient data.
    '''
    smoothed = smooth_data(data)
    gradient = np.gradient(np.array(smoothed, dtype=float), axis=0)
    norm = ([np.linalg.norm(i) for i in gradient])
    first_index = next(x[0] for x in enumerate(norm) if x[1] >= 1)
    last_index = len(norm) - next(
        x[0] for x in enumerate(reversed(norm)) if x[1] >= 1)
    return data[first_index:last_index]
