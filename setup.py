import os
import sys
import importlib.util
from pathlib import Path
import subprocess

def generate_sample_data():
    spec = importlib.util.spec_from_file_location("sample_sensor_data", "data/sample_sensor_data.py")
    sample_data_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sample_data_module)
    sample_data_module.generate_sample_data()
        
    print("Dữ liệu cảm biến mẫu đã được tạo thành công")
    return True

def create_maintenance_templates():
    print("Tạo các mẫu khuyến nghị bảo trì...")
    
    spec = importlib.util.spec_from_file_location("maintenance_templates", "data/maintenance_templates.py")
    templates_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(templates_module)
    templates_module.save_templates()

    return True

def create_model_configs():
    print("Tạo cấu hình mô hình và mô hình huấn luyện !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!.")
    spec = importlib.util.spec_from_file_location("model_config", "models/model_config.py")
    model_config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model_config_module)
    model_config_module.save_model_configs()
        
    model_config_module.create_pretrained_models()
        
    print("Cấu hình mô hình và mô hình huấn luyện trước đã được tạo thành công!")
    return True


def main():
    create_directory_structure()
    generate_sample_data()
    create_maintenance_templates()
    create_model_configs()


if __name__ == "__main__":
    main()
