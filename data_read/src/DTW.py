import time
import csv
import numpy as np


def calculate_gradient(data):
    return np.gradient(np.array(data, dtype=float), axis=0)


def read_csv(directory):
    result = []
    with open(directory, 'r') as infile:
        reader = csv.reader(infile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:  # each row is a list
            result.append(row)
    return result


def dtw_distance(live_data, directory):
    recorded_data = read_csv(directory)
    np_recorded_data = np.array(recorded_data)

    if live_data is None:
        return None

    if len(live_data) > 10:
        distance, _ = fastdtw(live_data, np_recorded_data)
        return distance
    else:
        return None


def check_gesture(total_data):
    while True:
        time.sleep(0.1)
        (gesture, first_index, last_index) = get_active_gesture(total_data)
        if first_index is not None and last_index is not None:
            distance = dtw_distance(gesture, '../data/data490.csv')
            print(distance)


def get_active_gesture(total_data):
    smoothed = smooth_data(total_data)
    gradient = calculate_gradient(smoothed)
    norm = list(reversed([np.linalg.norm(i) for i in gradient]))
    first_index = next((x[0] for x in enumerate(norm) if x[1] >= 1.5), None)
    if first_index is None:
        return (None, None, None)
    sub_norm = norm[first_index + 1:]
    last_sub_index = next(
        (x[0] for x in enumerate(sub_norm) if x[1] <= 0.5 and x[0] > 10), None)
    if last_sub_index is None:
        last_sub_index = len(sub_norm) - 1
    last_index = norm.index(sub_norm[last_sub_index])
    np_total_data = np.array(list(reversed(total_data)))
    gesture = list(reversed(np_total_data[first_index:last_index]))
    return (gesture, first_index, last_index)
