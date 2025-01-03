import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class AnomalyDetector:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.training_data = []

    def train_model(self, data):
        """Train or update the anomaly detection model with new data."""
        self.training_data.extend(data)
        if len(self.training_data) >= 100:  # Ensure we have enough data to train
            scaled_data = self.scaler.fit_transform(self.training_data)
            self.model.fit(scaled_data)
            self.training_data = []  # Reset for the next batch

    def check_anomaly(self, data_point):
        """Check if the new data point is an anomaly."""
        # If we haven't trained the model yet, train it with the first few data points
        if not hasattr(self.model, 'estimators_') or self.model.estimators_ is None:
            self.train_model([data_point])
            return 0, False  # Assume not an anomaly since we just trained on it
        
        # Scale the new data point
        scaled_point = self.scaler.transform([data_point])
        
        # Predict if it's an anomaly
        anomaly_score = self.model.decision_function(scaled_point)[0]
        prediction = self.model.predict(scaled_point)
        
        # Isolation Forest returns -1 for anomalies
        is_anomaly = prediction[0] == -1
        
        # Train the model with this data point for future predictions
        self.train_model([data_point])
        
        return anomaly_score, is_anomaly
