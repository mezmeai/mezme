from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np

class MezmeAgent:
    def __init__(self, config):
        self.model_type = config.get('model_type', 'RandomForest')
        self.features = config.get('features', [])
        self.threshold = config.get('threshold', 0.5)
        self.scaler = StandardScaler()
        self.model = self._init_model()

    def _init_model(self):
        if self.model_type == "RandomForest":
            return RandomForestClassifier() if self.threshold is not None else RandomForestRegressor()
        raise ValueError(f"Unsupported model type: {self.model_type}")

    def process_data(self, data):
        # Assume data is a dictionary where keys are feature names
        data_array = np.array([data.get(feature, 0) for feature in self.features]).reshape(1, -1)
        
        # Scale the data
        scaled_data = self.scaler.fit_transform(data_array)

        # Make prediction or classification
        prediction = self.model.predict(scaled_data)
        if self.threshold is not None:  # Classification
            return "Anomaly" if prediction[0] == 1 else "Normal"
        else:  # Regression
            return float(prediction[0])

    def train(self, data):
        # Here you'd pass in training data to update the model. 
        # This method is left as a placeholder for where training would occur.
        pass
