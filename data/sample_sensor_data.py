"""
Script tạo dữ liệu cảm biến mẫu cho hệ thống bảo trì dự đoán.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data():
    """Tạo dữ liệu cảm biến mẫu và lưu vào file CSV."""
    # Tạo dữ liệu cho 2 tuần với 5 phút mỗi lần đọc
    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)
    timestamps = pd.date_range(start=start_date, end=end_date, freq='5min')
    
    # Danh sách thiết bị
    equipment_ids = ['PUMP-101', 'PUMP-102', 'COMPRESSOR-A1', 'COMPRESSOR-B2', 'VALVE-S22']
    
    # Khởi tạo DataFrame rỗng
    all_data = pd.DataFrame()
    
    for equipment_id in equipment_ids:
        # Tạo dữ liệu cho mỗi thiết bị
        df = pd.DataFrame({'timestamp': timestamps})
        df['equipment_id'] = equipment_id
        
        # Tạo giá trị cơ bản cho từng loại thiết bị
        if 'PUMP' in equipment_id:
            temp_base = 65
            pressure_base = 100
            vibration_base = 0.5
            flow_base = 150
            power_base = 75
        elif 'COMPRESSOR' in equipment_id:
            temp_base = 75
            pressure_base = 120
            vibration_base = 0.7
            flow_base = 200
            power_base = 90
        else:  # VALVE
            temp_base = 45
            pressure_base = 85
            vibration_base = 0.3
            flow_base = 110
            power_base = 40
        
        # Thêm biến động ngẫu nhiên quanh giá trị cơ bản
        df['temperature'] = np.random.normal(temp_base, temp_base * 0.08, size=len(df))
        df['pressure'] = np.random.normal(pressure_base, pressure_base * 0.1, size=len(df))
        df['vibration'] = np.random.normal(vibration_base, vibration_base * 0.15, size=len(df))
        df['flow_rate'] = np.random.normal(flow_base, flow_base * 0.12, size=len(df))
        df['power_consumption'] = np.random.normal(power_base, power_base * 0.09, size=len(df))
        
        # Thêm xu hướng theo thời gian
        time_factor = np.linspace(0, 1, len(df))
        
        # Thêm các bất thường
        if equipment_id == 'PUMP-102':
            # Bắt đầu với nhiệt độ cao và giảm dần (lỗi làm mát)
            df['temperature'] += 15 * np.exp(-3 * time_factor)
            
        if equipment_id == 'COMPRESSOR-A1':
            # Tăng dần độ rung (đang phát triển lỗi cơ khí)
            anomaly_start = int(len(df) * 0.7)
            df.loc[anomaly_start:, 'vibration'] += np.linspace(0, 1.5, len(df) - anomaly_start)
            
        if equipment_id == 'VALVE-S22':
            # Sụt giảm đột ngột lưu lượng (van bị kẹt một phần)
            anomaly_start = int(len(df) * 0.6)
            df.loc[anomaly_start:, 'flow_rate'] *= 0.7
            
        # Thêm các bất thường ngẫu nhiên
        anomaly_indices = np.random.choice(range(len(df)), size=int(0.02 * len(df)), replace=False)
        
        if 'PUMP' in equipment_id:
            df.loc[anomaly_indices, 'temperature'] *= 1.2
            df.loc[anomaly_indices, 'vibration'] *= 1.5
        elif 'COMPRESSOR' in equipment_id:
            df.loc[anomaly_indices, 'pressure'] *= 1.25
            df.loc[anomaly_indices, 'power_consumption'] *= 1.3
        else:  # VALVE
            df.loc[anomaly_indices, 'flow_rate'] *= 0.6
            
        # Thêm ngày bảo trì cuối cùng (ngẫu nhiên trong khoảng 30-120 ngày trước)
        df['last_maintenance'] = start_date - timedelta(days=np.random.randint(30, 120))
        
        # Thêm vào DataFrame chính
        all_data = pd.concat([all_data, df])
    
    # Đảm bảo thư mục tồn tại
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Lưu vào file CSV
    csv_path = "data/sensor_data.csv"
    all_data.to_csv(csv_path, index=False)
    print(f"Đã tạo dữ liệu mẫu tại: {csv_path}")
    print(f"Tổng số dòng dữ liệu: {len(all_data)}")
    
    # Tạo một tập mẫu nhỏ hơn để dễ dàng kiểm tra
    sample = all_data.sample(n=min(1000, len(all_data)))
    sample.to_csv("data/sensor_data_sample.csv", index=False)
    
    return csv_path

if __name__ == "__main__":
    generate_sample_data()