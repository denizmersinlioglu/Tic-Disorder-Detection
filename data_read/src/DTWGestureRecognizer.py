import os
import GRT

DATA_DIMENSION = 6


class DTWGestureRecognizer:
    __instance = None

    @staticmethod
    def shared():
        ''' Static access method. '''
        if DTWGestureRecognizer.__instance is None:
            DTWGestureRecognizer()
        return DTWGestureRecognizer.__instance

    def __init__(self):
        ''' Virtually private constructor. '''
        if DTWGestureRecognizer.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.pipeline = GRT.GestureRecognitionPipeline()
            self.active_data = []
            self.pipeline.setClassifier(self.dtw_classifier())
            self.pipeline.classificationData = GRT.TimeSeriesClassificationData(
            )
            self.pipeline.classificationData.setDatasetName("Gesture_Data_Set")
            self.pipeline.trainingData = GRT.TimeSeriesClassificationData()
            self.pipeline.classificationData.setNumDimensions(DATA_DIMENSION)
            DTWGestureRecognizer.__instance = self

    def predict(self, data):
        '''
        Predicts input data according to trained data with DTW algorithm.
        Args:
            data (numpy.array): 6 axis accelerometer data.

        Returns:
            Int: Gesture Key. (None if pipeline is not trained yet)
        '''
        if self.pipeline.getTrained():
            result = self.pipeline.predict(data)
            if result:
                label = self.pipeline.getPredictedClassLabel()
                if label != -1:
                    print(label)
            else:
                print("prediction failed")
        else:
            return None

    def add_sample_data(self, key, sample):
        '''
        Adds sample data to related gesture when a key is pressed. 
        The sample data will be appended to classification data for DTW algorithm.
        As you add a sample data to pipeline it will train the DTW algorithm.
        Args:
            key (int): Related gesture key.
            sample (numpy.array): Gesture sample data. It should be np.matrix to be meaningful.

        Returns:
            bool: The return value. True for success, False otherwise.
        '''
        result = self.pipeline.classificationData.addSample(key, sample)
        print("STATS :", self.pipeline.classificationData.getStatsAsString())
        self.save_classification_data()
        self.save_pipeline()
        self.pipeline.train(self.pipeline.classificationData)
        return result

    def train_pipeline(self):
        # self.pipeline.trainingData = self.pipeline.classificationData.split(80)
        train_success = self.pipeline.train(self.pipeline.classificationData)

        # print("STATS :", self.pipeline.classificationData.getStatsAsString())
        # test_results = self.pipeline.getTestResults()

        # print("Pipeline Test Accuracy: ", self.pipeline.getTestAccuracy())
        # class_labels = self.pipeline.getClassLabels()

        # print("Precision: ")
        # for element in range(self.pipeline.getNumClassesInModel()):
        #     print("\t", self.pipeline.getTestPrecision(class_labels[element]))

        return train_success

    def save_pipeline(self):
        '''
        Saves the current pipline to ../dtw_data directory.

        Returns:
            bool: The return value. True for success, False otherwise.

        Raises:
            PipelineError: if pipeline save failed.

        '''
        pipeline_url = '../dtw_data/traing.grt'
        try:
            os.remove(pipeline_url)
        except Exception as exception:
            print(exception)

        result = self.pipeline.save(pipeline_url)
        if result:
            print("Pipeline saved.")
        else:
            print("Pipeline save failed.")

    def save_classification_data(self):
        '''
        Saves the dataset  to ../trainingData.csv directory.

        Returns:
            bool: The return value. True for success, False otherwise.

        Raises:
            ClassificationDataError: if classification data save failed.

        '''
        classification_data_url = '../dtw_data/trainingData.csv'
        try:
            os.remove(classification_data_url)
        except Exception as exception:
            print(exception)

        print(self.pipeline.classificationData)
        result = self.pipeline.classificationData.save(classification_data_url)

        if result:
            print("Classification data saved.")
        else:
            print("Classification data save failed.")

    def load_pipeline(self):
        '''
        Load a gesture recognition pipline from ../dtw_data directory.

        Returns:
            bool: The return value. True for success, False otherwise.

        Raises:
            PipelineError: if pipeline save failed.
            ClassificationDataError: if classification data save failed.

        '''
        pipeline_url = '../dtw_data/traing.grt'
        classification_data_url = '../dtw_data/trainingData.csv'
        try:
            os.remove(pipeline_url)
        except Exception as exception:
            print(exception)

        pipeline_result = self.pipeline.load(pipeline_url)
        if pipeline_result:
            return True
        else:
            raise Exception("Pipeline load failed.")

        classification_result = self.pipeline.loadClassificationData(
            classification_data_url)

        if classification_result:
            return True
        else:
            raise Exception("Classification data load failed.")

    def dtw_classifier(self):
        '''
        Built in DTW classifier of GRT Module. 
        Appropriate modifications was handled in default call.

        Returns:
            A DTW_Classifier from GRT LIB.
        '''
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

        return classifier