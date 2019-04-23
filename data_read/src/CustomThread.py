import threading
import time
import numpy as np
from DTWGestureRecognizer import DTWGestureRecognizer
from Utils import *


class PredictionThread(threading.Thread):
    def predict_gesture(self):
        try:
            data = np.array(DTWGestureRecognizer.shared().active_data)
            cropped = crop_active_gesture(data)
            if len(cropped) > 10:
                smoothed = smooth_data(cropped)
                sample = np.array(smoothed)
                prediction = DTWGestureRecognizer.shared().predict(sample)
                if prediction is not None:
                    print("Active Gesture Founded: Label: ", prediction)
        except Exception as ex:
            pass

    def run(self):
        while True:
            self.predict_gesture()
            time.sleep(0.1)


class ClassificationSampleThread(threading.Thread):
    def __init__(self, key, sample):
        self.key = key
        self.sample = sample
        threading.Thread.__init__(self)

    def run(self):
        result = DTWGestureRecognizer.shared().add_sample_data(
            self.key, self.sample)
        if result:
            print("Sample successfuly data added to the classification data")
        else:
            print("Sample successfuly data added to the classification data")

        # traning_thread = TrainingThread()
        # traning_thread.start()


class TrainingThread(threading.Thread):
    def run(self):
        result = DTWGestureRecognizer.shared().train_pipeline()
        if result:
            DTWGestureRecognizer.shared().save_pipeline()
            print("Pipeline succesfully trained")
        else:
            print("Pipeline train failed")
