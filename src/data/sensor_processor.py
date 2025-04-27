"""
Module để xử lý và làm sạch dữ liệu cảm biến từ thiết bị dầu khí.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler

class SensorDataProcessor:
    """Process and clean sensor data from oil and gas equipment."""
    
    def __init__(self, data_path: str = None):
        self.data_path = data_path
        self.data = None
        self.scaler = StandardScaler()
        
    def load_data(self, data_path: str = None) -> pd.DataFrame:
        """Load data from CSV file """
        if data_path:
            self.data_path = data_path
            
        self.generate_synthetic_data()
            
        return self.data
    
    def generate_synthetic_data(self, n_samples: int = 5000) -> pd.DataFrame:
        """Generate synthetic sensor data for demonstration purposes."""
        # Generate timestamps for the past week with 1-minute intervals
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        timestamps = pd.date_range(start=start_date, end=end_date, freq='1min')
        
        # Create dataframe with timestamps
        df = pd.DataFrame({'timestamp': timestamps})
        
        # Equipment IDs
        equipment_ids = ['PUMP-101', 'PUMP-102', 'COMPRESSOR-A1', 'COMPRESSOR-B2', 'VALVE-S22']
        df['equipment_id'] = np.random.choice(equipment_ids, size=len(df))
        
        # Generate normal sensor readings with some random variations
        df['temperature'] = np.random.normal(65, 5, size=len(df))
        df['pressure'] = np.random.normal(100, 10, size=len(df))
        df['vibration'] = np.random.normal(0.5, 0.2, size=len(df))
        df['flow_rate'] = np.random.normal(150, 15, size=len(df))
        df['power_consumption'] = np.random.normal(75, 7, size=len(df))
        
        # Add some anomalies for specific equipment
        anomaly_idx = np.random.choice(range(len(df)), size=int(0.05 * len(df)), replace=False)
        df.loc[anomaly_idx, 'temperature'] += np.random.uniform(10, 20, size=len(anomaly_idx))
        df.loc[anomaly_idx, 'vibration'] += np.random.uniform(0.5, 1.5, size=len(anomaly_idx))
        
        # Add maintenance history
        df['last_maintenance'] = np.random.choice(
            pd.date_range(start=start_date - timedelta(days=90), end=end_date, freq='D'),
            size=len(df)
        )
        
        self.data = df
        return df
    
    def preprocess_data(self) -> pd.DataFrame:
        """Clean and preprocess the sensor data."""
        if self.data is None:
            self.load_data()
            
        # Convert timestamp to datetime if it's not already
        if not pd.api.types.is_datetime64_any_dtype(self.data['timestamp']):
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
            
        # Handle missing values
        self.data.fillna(method='ffill', inplace=True)
        
        # Calculate time since last maintenance
        self.data['days_since_maintenance'] = (
            pd.to_datetime(self.data['timestamp']) - pd.to_datetime(self.data['last_maintenance'])
        ).dt.days
        
        # Normalize numerical features
        numerical_features = ['temperature', 'pressure', 'vibration', 'flow_rate', 'power_consumption']
        self.data[numerical_features] = self.scaler.fit_transform(self.data[numerical_features])
        
        return self.data
    
    def get_equipment_data(self, equipment_id: str) -> pd.DataFrame:
        """Filter data for a specific equipment."""
        if self.data is None:
            self.preprocess_data()
            
        return self.data[self.data['equipment_id'] == equipment_id]