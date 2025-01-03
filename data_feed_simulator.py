import numpy as np
import time

class DataFeedSimulator:
    def __init__(self):
        self.counter = 0

    def get_next_data_point(self):
        # Simulate a data feed with occasional anomalies
        self.counter += 1
        if self.counter % 10 == 0:  # Every 10th data point is potentially anomalous
            return np.array([np.random.uniform(10, 20), np.random.uniform(100, 200)]) + np.random.uniform(50, 100)
        else:
            return np.array([np.random.uniform(10, 20), np.random.uniform(100, 200)])
