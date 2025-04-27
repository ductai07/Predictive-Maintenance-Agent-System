"""
Các mẫu khuyến nghị bảo trì cho các tình huống bất thường khác nhau.
"""
import json
import os

# Các mẫu khuyến nghị cho các loại thiết bị khác nhau
MAINTENANCE_TEMPLATES = {
    "PUMP": {
        "high_temperature": {
            "issue": "Nhiệt độ bơm cao bất thường",
            "recommendation": "Kiểm tra hệ thống làm mát, mức dầu bôi trơn và căn chỉnh trục bơm. Cân nhắc vệ sinh bộ tản nhiệt.",
            "severity": "high",
            "consequences": "Có thể dẫn đến hỏng bạc đạn, biến dạng trục, và ngừng hoạt động hoàn toàn của bơm.",
            "estimated_downtime_hours": 6,
            "parts_needed": ["Dầu bôi trơn", "Bạc đạn", "Làm sạch hệ thống làm mát"]
        },
        "high_vibration": {
            "issue": "Độ rung cao bất thường",
            "recommendation": "Kiểm tra căn chỉnh trục, cân bằng rô-to, và kiểm tra tình trạng bạc đạn.",
            "severity": "high",
            "consequences": "Có thể gây hư hỏng cơ khí nghiêm trọng, rò rỉ đệm kín và sớm hỏng bạc đạn.",
            "estimated_downtime_hours": 8,
            "parts_needed": ["Bạc đạn mới", "Đệm kín trục", "Dụng cụ cân bằng"]
        },
        "low_flow_rate": {
            "issue": "Lưu lượng thấp bất thường",
            "recommendation": "Kiểm tra cánh bơm bị mòn, tắc nghẽn đường ống hút hoặc xả, và van điều khiển.",
            "severity": "medium",
            "consequences": "Giảm hiệu suất hệ thống và tăng áp lực không cần thiết trên động cơ bơm.",
            "estimated_downtime_hours": 4,
            "parts_needed": ["Bộ lọc", "Van một chiều", "Cánh bơm (nếu cần)"]
        }
    },
    "COMPRESSOR": {
        "high_temperature": {
            "issue": "Nhiệt độ máy nén cao bất thường",
            "recommendation": "Kiểm tra hệ thống làm mát, mức dầu bôi trơn và lọc khí. Cân nhắc vệ sinh bộ tản nhiệt.",
            "severity": "high",
            "consequences": "Có thể dẫn đến hư hỏng các thành phần nội bộ và giảm tuổi thọ thiết bị đáng kể.",
            "estimated_downtime_hours": 8,
            "parts_needed": ["Dầu bôi trơn", "Lọc dầu", "Lọc khí", "Làm sạch bộ trao đổi nhiệt"]
        },
        "high_power_consumption": {
            "issue": "Tiêu thụ điện năng cao bất thường",
            "recommendation": "Kiểm tra hiệu suất máy nén, độ rò rỉ hệ thống, và áp suất đẩy. Cân nhắc thay van xả.",
            "severity": "medium",
            "consequences": "Tăng chi phí vận hành và có thể là dấu hiệu của sự cố nghiêm trọng hơn.",
            "estimated_downtime_hours": 5,
            "parts_needed": ["Van xả", "Van an toàn", "Các phụ kiện điện"]
        },
        "pressure_fluctuation": {
            "issue": "Biến động áp suất bất thường",
            "recommendation": "Kiểm tra van điều khiển, cài đặt áp suất và rò rỉ trong hệ thống.",
            "severity": "medium",
            "consequences": "Có thể ảnh hưởng đến chất lượng sản phẩm và gây mòn sớm cho các thành phần.",
            "estimated_downtime_hours": 6,
            "parts_needed": ["Van điều áp", "Đệm kín", "Cảm biến áp suất"]
        }
    },
    "VALVE": {
        "leakage": {
            "issue": "Rò rỉ van",
            "recommendation": "Thay thế đệm kín, kiểm tra bề mặt tiếp xúc và trùng khớp của van. Cân nhắc mài lại bề mặt tiếp xúc.",
            "severity": "medium",
            "consequences": "Mất áp suất, tăng tiêu thụ năng lượng và có thể gây ô nhiễm hoặc mất sản phẩm.",
            "estimated_downtime_hours": 3,
            "parts_needed": ["Bộ đệm kín van", "Vật liệu mài", "Chất bôi trơn cho van"]
        },
        "stuck_valve": {
            "issue": "Van kẹt hoặc khó thao tác",
            "recommendation": "Tháo, vệ sinh và bôi trơn van. Kiểm tra cơ cấu truyền động và bộ điều khiển.",
            "severity": "high",
            "consequences": "Có thể dẫn đến mất kiểm soát quá trình, gây hư hỏng dây chuyền hoặc sản phẩm.",
            "estimated_downtime_hours": 4,
            "parts_needed": ["Bộ phận truyền động", "Chất bôi trơn", "Phụ tùng điều khiển"]
        },
        "control_failure": {
            "issue": "Lỗi điều khiển van",
            "recommendation": "Kiểm tra bộ điều khiển van, cảm biến phản hồi và kết nối. Hiệu chỉnh lại nếu cần thiết.",
            "severity": "high",
            "consequences": "Mất khả năng điều khiển chính xác quá trình, có thể gây ngừng sản xuất hoặc sự cố an toàn.",
            "estimated_downtime_hours": 6,
            "parts_needed": ["Bộ điều khiển van", "Cáp tín hiệu", "Cảm biến vị trí"]
        }
    }
}

def save_templates():
    """Lưu các mẫu khuyến nghị bảo trì vào file JSON."""
    # Đảm bảo thư mục tồn tại
    os.makedirs("data/templates", exist_ok=True)
    
    # Lưu tất cả các mẫu vào một file
    with open("data/templates/maintenance_templates.json", "w") as f:
        json.dump(MAINTENANCE_TEMPLATES, f, indent=4)
    
    # Lưu các mẫu riêng biệt cho từng loại thiết bị
    for equipment_type, templates in MAINTENANCE_TEMPLATES.items():
        with open(f"data/templates/{equipment_type.lower()}_templates.json", "w") as f:
            json.dump(templates, f, indent=4)
    
    print("Đã lưu các mẫu khuyến nghị bảo trì thành công!")
    return "data/templates/maintenance_templates.json"

def load_templates(equipment_type=None):
    """Tải các mẫu khuyến nghị bảo trì từ file JSON."""
    try:
        if equipment_type:
            with open(f"data/templates/{equipment_type.lower()}_templates.json", "r") as f:
                return json.load(f)
        else:
            with open("data/templates/maintenance_templates.json", "r") as f:
                return json.load(f)
    except FileNotFoundError:
        print("File mẫu khuyến nghị không tồn tại. Tạo các mẫu mới...")
        save_templates()
        return load_templates(equipment_type)

if __name__ == "__main__":
    save_templates()