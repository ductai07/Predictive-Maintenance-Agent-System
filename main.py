import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
from src.data.sensor_processor import SensorDataProcessor
from src.models.anomaly_detector import AnomalyDetector
from src.advisors.llm_advisor import LLMAdvisor
from src.agents.maintenance_agent import MaintenanceAgent
from src.ui.maintenance_dashboard import MaintenanceDashboard

def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    agent = MaintenanceAgent(api_key=api_key)
    agent.initialize_system()
    agent.process_all_equipment()
    
    # Khởi động bảng điều khiển
    dashboard = MaintenanceDashboard(agent)
    dashboard.run()


if __name__ == "__main__":
    main()
