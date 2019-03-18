from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import numpy as np


def dtw_distance(x, y):
    x = np.array(x)
    y = np.array(y)
    distance, path = fastdtw(x, y, dist=euclidean)
    return distance
