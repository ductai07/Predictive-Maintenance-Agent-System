# Predictive Maintenance Agent System - Hệ thống Bảo trì Dự đoán

Hệ thống bảo trì dự đoán cho thiết bị dầu khí sử dụng AI và phân tích dữ liệu để phát hiện sớm các bất thường và đề xuất kế hoạch bảo trì tối ưu.

## Mục đích và Chức năng

Hệ thống Bảo trì Dự đoán FPT Digital được thiết kế nhằm giải quyết các thách thức quan trọng trong vận hành và bảo trì thiết bị dầu khí. Trong các môi trường công nghiệp này, sự cố thiết bị không lường trước có thể dẫn đến thiệt hại kinh tế đáng kể, rủi ro an toàn và tác động môi trường nghiêm trọng.

### Mục đích

- **Giảm thiểu thời gian ngừng hoạt động ngoài kế hoạch**: Phát hiện sớm các dấu hiệu hỏng hóc tiềm ẩn trước khi chúng dẫn đến sự cố nghiêm trọng
- **Tối ưu hóa chu kỳ bảo trì**: Thay thế lịch bảo trì định kỳ cứng nhắc bằng kế hoạch bảo trì linh hoạt dựa trên tình trạng thực tế của thiết bị
- **Kéo dài tuổi thọ thiết bị**: Giám sát chính xác và can thiệp kịp thời giúp thiết bị hoạt động hiệu quả trong thời gian dài hơn
- **Nâng cao an toàn vận hành**: Giảm thiểu rủi ro sự cố đột ngột có thể gây nguy hiểm cho nhân viên hoặc môi trường
- **Tối ưu hóa chi phí bảo trì**: Giảm chi phí bảo trì không cần thiết và chi phí liên quan đến sự cố thiết bị

### Quy trình hoạt động

1. **Thu thập dữ liệu**: Hệ thống liên tục thu thập dữ liệu từ các cảm biến gắn trên thiết bị dầu khí, bao gồm nhiệt độ, áp suất, độ rung, lưu lượng và tiêu thụ điện năng (cái này dữ liệu demo tự sinh !!).

2. **Xử lý và chuẩn hóa dữ liệu**: Dữ liệu thô được làm sạch, chuẩn hóa và chuẩn bị cho phân tích nâng cao thông qua module SensorDataProcessor.

3. **Phát hiện bất thường**: Các mô hình học máy (chủ yếu sử dụng Isolation Forest) phân tích dữ liệu để xác định các mẫu bất thường có thể chỉ ra sự cố tiềm ẩn.

4. **Phân tích chuyên sâu**: Khi phát hiện bất thường, hệ thống sử dụng mô hình ngôn ngữ lớn (LLM) để phân tích nguyên nhân gốc rễ và đề xuất các hành động bảo trì phù hợp.

5. **Lập kế hoạch bảo trì**: Dựa trên mức độ nghiêm trọng và tính cấp bách của các vấn đề được phát hiện, hệ thống tạo kế hoạch bảo trì tối ưu để giảm thiểu thời gian dừng máy.

6. **Giám sát và cập nhật liên tục**: Hệ thống liên tục theo dõi hiệu quả của các can thiệp bảo trì và cập nhật mô hình phân tích để cải thiện hiệu suất theo thời gian.

### Các chức năng chi tiết

- **Giám sát trạng thái thiết bị theo thời gian thực**: Bảng điều khiển trực quan hiển thị các chỉ số quan trọng và cảnh báo khi phát hiện bất thường
- **Phân loại mức độ nghiêm trọng**: Tự động phân loại các vấn đề theo thang độ nghiêm trọng (thấp, trung bình, cao, nguy cấp) dựa trên phân tích dữ liệu
- **Khuyến nghị bảo trì thông minh**: Cung cấp hướng dẫn chi tiết về các hành động bảo trì cần thực hiện, bao gồm cả danh sách phụ tùng cần thiết
- **Ước tính thời gian ngừng hoạt động**: Dự đoán thời gian cần thiết để thực hiện các nhiệm vụ bảo trì
- **Lập lịch bảo trì tích hợp**: Cho phép người dùng lên lịch bảo trì và phân công nhóm kỹ thuật trực tiếp từ bảng điều khiển
- **Phân tích dự báo**: Xác định các xu hướng dài hạn và mô hình hỏng hóc tiềm ẩn để cải thiện chiến lược bảo trì
- **Tối ưu hóa kế hoạch bảo trì**: Sắp xếp lịch bảo trì cho nhiều thiết bị để giảm thiểu tổng thời gian ngừng hoạt động

## Tính năng chính

- **Xử lý dữ liệu cảm biến**: Thu thập và xử lý dữ liệu từ các cảm biến thiết bị dầu khí
- **Phát hiện bất thường**: Sử dụng mô hình học máy để phát hiện các hoạt động bất thường của thiết bị
- **Cố vấn bảo trì thông minh**: Phân tích bất thường và đưa ra các khuyến nghị bảo trì dựa trên LLM
- **Kế hoạch bảo trì tối ưu**: Tự động lập kế hoạch bảo trì để giảm thiểu thời gian ngừng hoạt động
- **Bảng điều khiển trực quan**: Giao diện tương tác để giám sát trạng thái thiết bị và quản lý bảo trì

## Cấu trúc dự án

```
Predictive Maintenance Agent System/
│
├── main.py                     # Điểm khởi chạy chính của ứng dụng
├── README.md                  # File hướng dẫn
├── requirements.txt           # Các thư viện phụ thuộc
│
├── src/                       # Mã nguồn chính
│   ├── __init__.py
│   ├── data/                  # Mô-đun xử lý dữ liệu
│   │   ├── __init__.py
│   │   └── sensor_processor.py
│   │
│   ├── models/                # Mô-đun mô hình học máy
│   │   ├── __init__.py
│   │   └── anomaly_detector.py
│   │
│   ├── advisors/             # Mô-đun cố vấn bảo trì
│   │   ├── __init__.py
│   │   └── llm_advisor.py
│   │
│   ├── agents/               # Mô-đun đại lý bảo trì
│   │   ├── __init__.py
│   │   └── maintenance_agent.py
│   │
│   └── ui/                   # Mô-đun giao diện người dùng
│       ├── __init__.py
│       └── maintenance_dashboard.py
│
├── data/                     # Dữ liệu mẫu và các tài nguyên
│   ├── sample_sensor_data.py  # Script tạo dữ liệu cảm biến mẫu
│   ├── maintenance_templates.py  # Mẫu khuyến nghị bảo trì
│   ├── templates/            # Thư mục chứa các template JSON
│   └── sensor_data.csv       # Dữ liệu cảm biến được tạo
│
└── models/                   # Mô hình đã huấn luyện và cấu hình
    ├── model_config.py       # Cấu hình mô hình 
    └── configs/              # Thư mục chứa cấu hình JSON 
```

## Cài đặt

1. Clone repository:

```bash
git clone [https://github.com/fptdigital/predictive-maintenance.git](https://github.com/ductai07/Predictive-Maintenance-Agent-System)
```

2. Cài đặt các dependencies:

```bash
pip install -r requirements.txt
```

3. Tạo dữ liệu mẫu:

```bash
python data/sample_sensor_data.py
```

4. Cấu hình mô hình:

```bash
python models/model_config.py
```
Demo UI
![Demo](https://github.com/ductai07/Predictive-Maintenance-Agent-System/blob/master/demo.gif)
