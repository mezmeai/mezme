import numpy as np
from sklearn.ensemble import IsolationForest
from data_feed_simulator import DataFeedSimulator
from anomaly_models import AnomalyDetector

class MezmeAgent:
    def __init__(self):
        self.data_feed = DataFeedSimulator()
        self.anomaly_detector = AnomalyDetector()

    def monitor_data_feed(self):
        """Continuously monitor the data feed for anomalies."""
        while True:
            data_point = self.data_feed.get_next_data_point()
            anomaly_score, is_anomaly = self.anomaly_detector.check_anomaly(data_point)
            
            if is_anomaly:
                print(f"Anomaly detected! Data point: {data_point}, Anomaly Score: {anomaly_score}")
                # Here we would implement actions like alerting or pausing smart contract execution
            else:
                print(f"Normal data point: {data_point}, Anomaly Score: {anomaly_score}")
            
            # In a real-world scenario, you might want to add a sleep function here to control frequency

if __name__ == "__main__":
    mezme = MezmeAgent()
    mezme.monitor_data_feed()
