import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
import json
from datetime import datetime, timedelta

class MezmeAnalyzer:
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()

    def prepare_data(self, data):
        # Convert data to a pandas DataFrame for easier manipulation
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.select_dtypes(include=[np.number])  # Only keep numeric columns for now

        # Remove any rows with NaN values since they would disrupt our model
        df = df.dropna()

        # Split into features and target. Here, we're assuming 'temperature' might be our target variable
        if 'temperature' in df.columns:
            X = df.drop('temperature', axis=1)
            y = df['temperature']
        else:
            # If no clear target, we use all data for unsupervised learning or anomaly detection
            X = df
            y = None

        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled, y, X.columns

    def train_regression_model(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"MezmeAnalyzer: Regression model MSE: {mse}")
        
        self.models['regression'] = model

    def train_classification_model(self, X, y):
        # Convert y to binary for classification (example: is temperature above average?)
        if y is not None:
            y_binary = (y > y.mean()).astype(int)
            X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            print(f"MezmeAnalyzer: Classification model Accuracy: {accuracy}")
            
            self.models['classification'] = model
        else:
            print("MezmeAnalyzer: No suitable target variable for classification.")

    def predict(self, new_data):
        if 'regression' in self.models:
            new_data_scaled = self.scaler.transform(new_data)
            prediction = self.models['regression'].predict(new_data_scaled)
            return {"type": "regression", "prediction": prediction[0]}
        elif 'classification' in self.models:
            new_data_scaled = self.scaler.transform(new_data)
            prediction = self.models['classification'].predict(new_data_scaled)
            return {"type": "classification", "prediction": "Above average" if prediction[0] == 1 else "Below average"}
        else:
            return {"type": "error", "message": "No model trained yet."}

    def analyze(self, data):
        X, y, features = self.prepare_data(data)
        
        if y is not None:
            self.train_regression_model(X, y)
            self.train_classification_model(X, y)
        else:
            print("MezmeAnalyzer: No target variable for supervised learning. Consider unsupervised methods.")
        
        # Example prediction - use the last row of data or create a new scenario
        if len(X) > 0:
            return self.predict(X[-1].reshape(1, -1))  # Predict based on the last data point
        else:
            return {"type": "error", "message": "No data for prediction."}

class MezmeDecisionMaker:
    def __init__(self):
        self.analyzer = MezmeAnalyzer()

    def decision_for_smart_contract(self, data):
        analysis = self.analyzer.analyze(data)
        if analysis['type'] == 'error':
            return {"decision": "Error in analysis", "details": analysis['message']}
        
        if analysis['type'] == 'regression':
            # Example decision based on temperature prediction
            if analysis['prediction'] > 25:  # Assuming 25°C as a threshold for high temperature
                return {"decision": "Activate cooling system", "details": f"Predicted temperature {analysis['prediction']:.2f}°C"}
            else:
                return {"decision": "Maintain current settings", "details": f"Predicted temperature {analysis['prediction']:.2f}°C"}
        
        if analysis['type'] == 'classification':
            if analysis['prediction'] == "Above average":
                return {"decision": "Adjust for higher than average conditions", "details": "Temperature predicted above average"}
            else:
                return {"decision": "Standard operations", "details": "Temperature predicted below average"}

def main():
    # Sample data - in practice, this would come from MezmeCollector or similar data source
    sample_data = {
        "sensor_001": {"temperature": 23.5, "humidity": 55.0},
        "sensor_002": {"temperature": 22.0, "humidity": 57.0},
        "api_data": {"temperature": 24.0, "humidity": 50.0},
        "traditional_data": {"temperature": 23.0, "humidity": 56.0}
    }

    decision_maker = MezmeDecisionMaker()
    decision = decision_maker.decision_for_smart_contract(sample_data)
    print(f"MezmeDecisionMaker: {json.dumps(decision, indent=2)}")

if __name__ == "__main__":
    main()
