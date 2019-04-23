import threading
import time
import numpy as np
from DTWGestureRecognizer import DTWGestureRecognizer


class PredictionThread(threading.Thread):
    def predict_gesture(self):
        try:
            sample = np.array(DTWGestureRecognizer.shared().active_data)
            # print(sample)
            DTWGestureRecognizer.shared().predict(sample)
        except Exception as ex:
            print(ex)

    def run(self):
        while True:
            self.predict_gesture()
            time.sleep(0.033)


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
