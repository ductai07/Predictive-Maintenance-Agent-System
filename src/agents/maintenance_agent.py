"""
Module chứa đại lý bảo trì chịu trách nhiệm điều phối xử lý dữ liệu, phát hiện bất thường và lập kế hoạch bảo trì.
"""
from typing import Dict, List

from src.data.sensor_processor import SensorDataProcessor
from src.models.anomaly_detector import AnomalyDetector
from src.advisors.llm_advisor import LLMAdvisor

class MaintenanceAgent:
    """Agent that coordinates data processing, anomaly detection, and maintenance planning."""
    
    def __init__(self, api_key: str = None):
        self.data_processor = SensorDataProcessor()
        self.anomaly_detector = AnomalyDetector()
        self.llm_advisor = LLMAdvisor(api_key)
        self.equipment_status = {}
        self.maintenance_recommendations = {}
        self.maintenance_plan = None
        
    def initialize_system(self, data_path: str = None) -> None:
        """Initialize the system with data."""
        # Load and preprocess data
        data = self.data_processor.load_data(data_path)
        self.data_processor.preprocess_data()
        
        # Train anomaly detection model
        self.anomaly_detector.train(data)
        
        # Initialize equipment status
        for equipment_id in data['equipment_id'].unique():
            self.equipment_status[equipment_id] = "Unknown"
    
    def process_equipment(self, equipment_id: str) -> Dict:
        """Process data for a specific equipment and generate recommendations."""
        # Get equipment data
        equipment_data = self.data_processor.get_equipment_data(equipment_id)
        
        # Detect anomalies
        equipment_data = self.anomaly_detector.detect_anomalies(equipment_data)
        
        # Analyze with LLM and get recommendations
        recommendation = self.llm_advisor.analyze_anomaly(equipment_data)
        
        # Calculate anomaly percentage
        anomaly_percentage = (equipment_data['is_anomaly'].sum() / len(equipment_data)) * 100
        
        # Determine status based on anomaly percentage
        if anomaly_percentage < 3:
            status = "low"
        elif anomaly_percentage < 7:
            status = "medium"
        elif anomaly_percentage < 15:
            status = "high"
        else:
            status = "critical"
        
        # Update equipment status and store recommendation
        self.equipment_status[equipment_id] = status
        self.maintenance_recommendations[equipment_id] = recommendation
        
        return recommendation
    
    def process_all_equipment(self) -> Dict:
        """Process all equipment and create a maintenance plan."""
        # Get list of all equipment
        all_equipment = list(self.equipment_status.keys())
        
        # Process each equipment
        for equipment_id in all_equipment:
            self.process_equipment(equipment_id)
        
        # Create maintenance plan
        self.maintenance_plan = self.llm_advisor.create_maintenance_plan(
            all_equipment, self.maintenance_recommendations
        )
        
        return {
            "equipment_status": self.equipment_status,
            "recommendations": self.maintenance_recommendations,
            "maintenance_plan": self.maintenance_plan
        }
    
    def get_equipment_details(self, equipment_id: str) -> Dict:
        """Get detailed information for a specific equipment."""
        equipment_data = self.data_processor.get_equipment_data(equipment_id)
        anomaly_data = self.anomaly_detector.detect_anomalies(equipment_data)
        
        # Calculate summary statistics
        summary = {
            "equipment_id": equipment_id,
            "total_readings": len(anomaly_data),
            "anomaly_count": anomaly_data['is_anomaly'].sum(),
            "anomaly_percentage": (anomaly_data['is_anomaly'].sum() / len(anomaly_data)) * 100,
            "avg_temperature": anomaly_data['temperature'].mean(),
            "avg_pressure": anomaly_data['pressure'].mean(),
            "avg_vibration": anomaly_data['vibration'].mean(),
            "avg_flow_rate": anomaly_data['flow_rate'].mean(),
            "avg_power_consumption": anomaly_data['power_consumption'].mean(),
            "days_since_maintenance": anomaly_data['days_since_maintenance'].mean(),
            "status": self.equipment_status.get(equipment_id, "Unknown"),
            "recommendation": self.maintenance_recommendations.get(equipment_id, {})
        }
        
        return {
            "summary": summary,
            "data": anomaly_data.to_dict(orient='records')
        }