"""
Module chứa các mô hình phát hiện bất thường của thiết bị.
"""
import pandas as pd
from sklearn.ensemble import IsolationForest
from typing import List

class AnomalyDetector:
    """Detect anomalies in equipment sensor data."""
    
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.is_trained = False
        
    def train(self, data: pd.DataFrame) -> None:
        """Train the anomaly detection model."""
        features = ['temperature', 'pressure', 'vibration', 'flow_rate', 'power_consumption']
        self.model.fit(data[features])
        self.is_trained = True
    
    def detect_anomalies(self, data: pd.DataFrame) -> pd.DataFrame:
        """Detect anomalies in the given data."""
        if not self.is_trained:
            self.train(data)
            
        # Create a copy of the DataFrame to avoid SettingWithCopyWarning
        result = data.copy()
        
        features = ['temperature', 'pressure', 'vibration', 'flow_rate', 'power_consumption']
        result.loc[:, 'anomaly_score'] = self.model.decision_function(result[features])
        result.loc[:, 'is_anomaly'] = self.model.predict(result[features]) == -1
        
        return result