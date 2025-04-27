"""
Script thiết lập ban đầu cho hệ thống bảo trì dự đoán.
Tạo thư mục cần thiết, tạo dữ liệu mẫu và mô hình huấn luyện trước.
"""
import os
import sys
import importlib.util
from pathlib import Path
import subprocess


def create_directory_structure():
    """Tạo cấu trúc thư mục cần thiết."""
    print("Tạo cấu trúc thư mục...")
    
    # Các thư mục cần tạo
    directories = [
        "data/templates",
        "models/configs",
        "models/pretrained"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
    print("✅ Cấu trúc thư mục đã được tạo thành công!")
    return True

def generate_sample_data():
    """Tạo dữ liệu cảm biến mẫu."""
    print("Tạo dữ liệu cảm biến mẫu...")
    
    spec = importlib.util.spec_from_file_location("sample_sensor_data", "data/sample_sensor_data.py")
    sample_data_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sample_data_module)
        
        # Gọi hàm tạo dữ liệu
    sample_data_module.generate_sample_data()
        
    print("Dữ liệu cảm biến mẫu đã được tạo thành công")
    return True

def create_maintenance_templates():
    """Tạo các mẫu khuyến nghị bảo trì."""
    print("Tạo các mẫu khuyến nghị bảo trì...")
    
    spec = importlib.util.spec_from_file_location("maintenance_templates", "data/maintenance_templates.py")
    templates_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(templates_module)
    templates_module.save_templates()
    print("✅ Các mẫu khuyến nghị bảo trì đã được tạo thành công!")
    return True

def create_model_configs():
    """Tạo cấu hình mô hình và mô hình huấn luyện trước."""
    print("Tạo cấu hình mô hình và mô hình huấn luyện trước...")
    
        # Import và chạy module model_config
    spec = importlib.util.spec_from_file_location("model_config", "models/model_config.py")
    model_config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model_config_module)
        
        # Gọi hàm tạo cấu hình
    model_config_module.save_model_configs()
        
        # Tạo mô hình huấn luyện trước
    model_config_module.create_pretrained_models()
        
    print("Cấu hình mô hình và mô hình huấn luyện trước đã được tạo thành công!")
    return True


def main():
    create_directory_structure()
    # Tạo dữ liệu mẫu và mẫu khuyến nghị
    generate_sample_data()
    create_maintenance_templates()
    
    # Tạo cấu hình mô hình
    create_model_configs()


if __name__ == "__main__":
    main()