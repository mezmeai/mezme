import requests
import json
from datetime import datetime
import random  # For simulating IoT data
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

class MezmeCollector:
    def __init__(self):
        self.collected_data = {}

    def collect_iot_data(self, device_id):
        # Simulating IoT data collection
        temp = random.uniform(20, 30)  # Temperature in Celsius
        humidity = random.uniform(40, 60)
        self.collected_data[device_id] = {
            "temperature": temp,
            "humidity": humidity,
            "timestamp": datetime.now().isoformat()
        }
        print(f"MezmeCollector: Collected IoT data from device {device_id}")

    def collect_api_data(self, api_url):
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            self.collected_data["api_data"] = response.json()
            print(f"MezmeCollector: Collected API data from {api_url}")
        except requests.RequestException as e:
            print(f"MezmeCollector: Failed to collect data from {api_url}: {e}")

    def collect_traditional_data(self, provider):
        # Simulating data from traditional data providers
        self.collected_data["traditional_data"] = {
            "temperature": random.uniform(10, 25),
            "condition": random.choice(["Sunny", "Cloudy", "Rainy"]),
            "timestamp": datetime.now().isoformat()
        }
        print(f"MezmeCollector: Collected traditional data from {provider}")

class MezmeVerifier:
    def __init__(self):
        self.scaler = StandardScaler()
        self.clf = IsolationForest(contamination=0.1, random_state=42)

    def verify_data(self, data):
        # Convert data to a format suitable for analysis
        features = []
        for source, values in data.items():
            if isinstance(values, dict):
                features.extend([v for v in values.values() if isinstance(v, (int, float))])
        
        if not features:
            print("MezmeVerifier: No numeric features to verify.")
            return True  # If there's no data to verify, assume it's valid
        
        # Scale features
        scaled_features = self.scaler.fit_transform(np.array(features).reshape(-1, 1))
        
        # Fit and predict anomalies
        self.clf.fit(scaled_features)
        predictions = self.clf.predict(scaled_features)
        
        # If any prediction is -1 (outlier), we consider the data as potentially inaccurate
        if -1 in predictions:
            print("MezmeVerifier: Warning: Some data points seem anomalous.")
            return False
        print("MezmeVerifier: Data verified as accurate and relevant.")
        return True

def main():
    # Initialize Mezme agents
    mezme_collector = MezmeCollector()
    mezme_verifier = MezmeVerifier()

    # Collect data with MezmeCollector
    mezme_collector.collect_iot_data("sensor_001")
    mezme_collector.collect_api_data("http://api.example.com/current_weather")
    mezme_collector.collect_traditional_data("national_weather_service")

    # Verify collected data with MezmeVerifier
    if mezme_verifier.verify_data(mezme_collector.collected_data):
        print("Mezmes have verified the data as accurate and relevant.")
        # Further processing or storage could go here
    else:
        print("Mezmes recommend rechecking the data collection process.")

if __name__ == "__main__":
    main()
