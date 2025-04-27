"""
Module chứa cố vấn bảo trì dựa trên LLM cho dữ liệu cảm biến bất thường.
"""
import os
import json
import pandas as pd
from typing import Dict, List
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

class LLMAdvisor:
    """Use LLM to analyze anomalies and provide maintenance recommendations."""
    
    def __init__(self, api_key: str = None):
        # If API key is provided, use it; otherwise rely on environment variables
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
            
        # Initialize OpenAI model
        self.llm = GoogleGenerativeAI(model="gemini-2.0-flash",temperature=0.1)
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        
    def analyze_anomaly(self, equipment_data: pd.DataFrame) -> Dict:
        """Analyze anomalies using LLM and generate recommendations."""
        # Filter only anomalous data points
        anomaly_data = equipment_data[equipment_data['is_anomaly']]
        
        if anomaly_data.empty:
            return {"recommendation": "Không phát hiện bất thường. Hoạt động bình thường.", "severity": "low"}
        
        # Prepare data for LLM analysis
        equipment_id = equipment_data['equipment_id'].iloc[0]
        avg_temp = anomaly_data['temperature'].mean()
        avg_pressure = anomaly_data['pressure'].mean()
        avg_vibration = anomaly_data['vibration'].mean()
        avg_flow = anomaly_data['flow_rate'].mean()
        avg_power = anomaly_data['power_consumption'].mean()
        days_since_maint = anomaly_data['days_since_maintenance'].mean()
        anomaly_count = len(anomaly_data)
        total_data_points = len(equipment_data)
        anomaly_percentage = (anomaly_count / total_data_points) * 100
        
        prompt = PromptTemplate(
            input_variables=["equipment_id", "data_summary"],
            template="""
            Bạn là chuyên gia tư vấn bảo trì thiết bị dầu khí. Hãy phân tích dữ liệu cảm biến sau
            và đưa ra khuyến nghị bảo trì chi tiết.
            
            Mã thiết bị: {equipment_id}
            
            Tóm tắt dữ liệu:
            {data_summary}
            
            Hãy đưa ra phân tích chi tiết bao gồm:
            1. Vấn đề có khả năng gây ra các bất thường này
            2. Hành động bảo trì được khuyến nghị
            3. Mức độ khẩn cấp (low-thấp, medium-trung bình, high-cao, critical-nguy cấp)
            4. Hậu quả tiềm ẩn nếu không được xử lý
            5. Thời gian dừng máy ước tính để bảo trì
            6. Các phụ tùng hoặc công cụ cần thiết
            
            Phản hồi của bạn phải ở định dạng JSON với các khóa: "issue", "recommendation", "severity", 
            "consequences", "estimated_downtime_hours", "parts_needed"
            
            Tất cả nội dung phải được viết bằng tiếng Việt có dấu đầy đủ.
            """
        )
        
        data_summary = f"""
        - Số bất thường được phát hiện: {anomaly_count} ({anomaly_percentage:.2f}% số đọc)
        - Nhiệt độ trung bình (chuẩn hóa): {avg_temp:.2f}
        - Áp suất trung bình (chuẩn hóa): {avg_pressure:.2f}
        - Độ rung trung bình (chuẩn hóa): {avg_vibration:.2f}
        - Lưu lượng trung bình (chuẩn hóa): {avg_flow:.2f}
        - Mức tiêu thụ điện trung bình (chuẩn hóa): {avg_power:.2f}
        - Số ngày kể từ lần bảo trì cuối: {days_since_maint:.0f}
        """
        
        chain = prompt|self.llm
        result = chain.invoke({"equipment_id":equipment_id, "data_summary":data_summary})
        
        try:
            # Clean and parse the JSON response
            result = result.replace("```json", "").replace("```", "").strip()
            recommendation = json.loads(result)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            recommendation = {
                "issue": "Thiết bị có thể gặp trục trặc",
                "recommendation": result,
                "severity": "medium" if anomaly_percentage > 10 else "low",
                "consequences": "Thiết bị có thể bị hỏng nếu không được xử lý",
                "estimated_downtime_hours": 4,
                "parts_needed": ["công cụ kiểm tra"]
            }
            
        return recommendation
    
    def create_maintenance_plan(self, equipment_list: List[str], recommendations: Dict) -> Dict:
        """Create an optimized maintenance plan for multiple equipment."""
        prompt = PromptTemplate(
            input_variables=["equipment_data"],
            template="""
            Bạn là một chuyên gia lập kế hoạch bảo trì cho các cơ sở dầu khí.
            Dựa trên các thiết bị và khuyến nghị bảo trì sau đây, hãy tạo một lịch trình bảo trì tối ưu 
            giúp giảm thiểu thời gian ngừng hoạt động và sử dụng hiệu quả các đội bảo trì.

            Thiết bị và Khuyến nghị:
            {equipment_data}
            
            Hãy tạo kế hoạch bảo trì ưu tiên với:
            1. Thứ tự các thiết bị cần được bảo trì
            2. Lý do cho việc sắp xếp ưu tiên
            3. Tổng thời gian ngừng hoạt động ước tính
            4. Danh sách tổng hợp phụ tùng cần thiết
            5. Đề xuất về quy mô và thành phần của đội bảo trì
            
            Phản hồi của bạn phải ở định dạng JSON với các khóa: "schedule", "justification", 
            "total_downtime_hours", "parts_list", "crew_requirements"
            
            Tất cả nội dung phải được viết bằng tiếng Việt có dấu đầy đủ.
            """
        )
        
        equipment_data = ""
        for equipment in equipment_list:
            if equipment in recommendations:
                rec = recommendations[equipment]
                equipment_data += f"""
                Thiết bị: {equipment}
                Vấn đề: {rec.get('issue', 'Không xác định')}
                Mức độ nghiêm trọng: {rec.get('severity', 'low')}
                Thời gian ngừng hoạt động ước tính: {rec.get('estimated_downtime_hours', 4)} giờ
                Phụ tùng cần thiết: {', '.join(rec.get('parts_needed', ['công cụ kiểm tra']))}
                
                """
        
        chain = prompt|self.llm
        result = chain.invoke({"equipment_data":equipment_data})
        
        try:
            # Clean and parse the JSON response
            result = result.replace("```json", "").replace("```", "").strip()
            plan = json.loads(result)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            plan = {
                "schedule": "Ưu tiên theo mức độ nghiêm trọng",
                "justification": "Các vấn đề nguy cấp phải được giải quyết trước",
                "total_downtime_hours": sum([rec.get('estimated_downtime_hours', 4) for rec in recommendations.values()]),
                "parts_list": list(set([part for rec in recommendations.values() for part in rec.get('parts_needed', ['công cụ kiểm tra'])])),
                "crew_requirements": "Đội bảo trì tiêu chuẩn"
            }
            
        return plan