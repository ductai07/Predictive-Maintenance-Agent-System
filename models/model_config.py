"""
Cấu hình và các tham số cho các mô hình phát hiện bất thường.
"""
import os
import json
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, Any

# Các cấu hình mô hình mặc định
DEFAULT_MODEL_CONFIGS = {
    "PUMP": {
        "isolation_forest": {
            "n_estimators": 120,
            "contamination": 0.07,
            "max_samples": 0.8,
            "random_state": 42
        },
        "feature_importance": {
            "temperature": 0.35,
            "vibration": 0.30,
            "pressure": 0.15,
            "flow_rate": 0.10,
            "power_consumption": 0.10
        }
    },
    "COMPRESSOR": {
        "isolation_forest": {
            "n_estimators": 150,
            "contamination": 0.05,
            "max_samples": 0.75,
            "random_state": 42
        },
        "feature_importance": {
            "temperature": 0.25,
            "vibration": 0.20,
            "pressure": 0.30,
            "flow_rate": 0.05,
            "power_consumption": 0.20
        }
    },
    "VALVE": {
        "isolation_forest": {
            "n_estimators": 100,
            "contamination": 0.03,
            "max_samples": 0.8,
            "random_state": 42
        },
        "feature_importance": {
            "temperature": 0.10,
            "vibration": 0.15,
            "pressure": 0.25,
            "flow_rate": 0.40,
            "power_consumption": 0.10
        }
    }
}

def save_model_configs():
    """Lưu các cấu hình mô hình mặc định vào file."""
    # Đảm bảo thư mục tồn tại
    os.makedirs("models/configs", exist_ok=True)
    
    # Lưu tất cả cấu hình vào một file
    with open("models/configs/model_configs.json", "w") as f:
        json.dump(DEFAULT_MODEL_CONFIGS, f, indent=4)
    
    # Lưu cấu hình riêng cho từng loại thiết bị
    for equipment_type, config in DEFAULT_MODEL_CONFIGS.items():
        with open(f"models/configs/{equipment_type.lower()}_config.json", "w") as f:
            json.dump(config, f, indent=4)
    
    print("Đã lưu các cấu hình mô hình thành công!")
    
def load_model_config(equipment_type: str = None) -> Dict[str, Any]:
    """Tải cấu hình mô hình từ file."""
    try:
        if equipment_type:
            with open(f"models/configs/{equipment_type.lower()}_config.json", "r") as f:
                return json.load(f)
        else:
            with open("models/configs/model_configs.json", "r") as f:
                return json.load(f)
    except FileNotFoundError:
        print("File cấu hình mô hình không tồn tại. Tạo cấu hình mặc định...")
        save_model_configs()
        return load_model_config(equipment_type)

def create_pretrained_models():
    """Tạo và lưu các mô hình đã được huấn luyện trước với dữ liệu tổng hợp."""
    os.makedirs("models/pretrained", exist_ok=True)
    
    for equipment_type, config in DEFAULT_MODEL_CONFIGS.items():
        print(f"Tạo mô hình cho thiết bị {equipment_type}...")
        
        # Tạo dữ liệu tổng hợp cho huấn luyện
        np.random.seed(42)
        n_samples = 1000
        
        # Tạo dữ liệu bình thường
        normal_data = np.random.normal(0, 1, size=(n_samples, 5))
        
        # Tạo một số dữ liệu bất thường (ngoại lai)
        anomaly_ratio = config['isolation_forest']['contamination']
        anomaly_count = int(anomaly_ratio * n_samples)
        anomaly_data = np.random.uniform(-5, 5, size=(anomaly_count, 5))
        
        # Kết hợp dữ liệu
        data = np.vstack([normal_data, anomaly_data])
        
        # Khởi tạo và huấn luyện mô hình
        model = IsolationForest(**config['isolation_forest'])
        model.fit(data)
        
        # Lưu mô hình
        joblib.dump(model, f"models/pretrained/{equipment_type.lower()}_model.joblib")
    
    print("Đã tạo và lưu các mô hình huấn luyện trước thành công!")

def load_pretrained_model(equipment_type: str):
    """Tải mô hình đã được huấn luyện trước."""
    try:
        model_path = f"models/pretrained/{equipment_type.lower()}_model.joblib"
        return joblib.load(model_path)
    except FileNotFoundError:
        print(f"Không tìm thấy mô hình cho thiết bị {equipment_type}. Tạo mô hình mới...")
        create_pretrained_models()
        return load_pretrained_model(equipment_type)

if __name__ == "__main__":
    save_model_configs()
    create_pretrained_models()