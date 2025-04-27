import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from src.agents.maintenance_agent import MaintenanceAgent

class MaintenanceDashboard:
    """Interactive dashboard for the predictive maintenance system."""
    
    def __init__(self, maintenance_agent: MaintenanceAgent):
        self.agent = maintenance_agent
        
    def run(self):
        """Run the Streamlit dashboard."""
        st.set_page_config(page_title="Hệ Thống Bảo Trì Dự Đoán Dầu Khí", layout="wide")
        
        st.title("🛢️ Hệ Thống Bảo Trì Dự Đoán Dầu Khí")
        st.markdown("""
        Hệ thống hỗ trợ AI này giám sát tình trạng thiết bị, phát hiện bất thường và đưa ra 
        các khuyến nghị bảo trì để ngăn chặn thời gian ngừng hoạt động tốn kém.
        """)
        
        # Initialize system if not already done
        if not self.agent.equipment_status:
            self.agent.initialize_system()
        
        # Sidebar for controls
        st.sidebar.header("Điều Khiển")
        
        # Equipment selection
        equipment_list = list(self.agent.equipment_status.keys())
        selected_equipment = st.sidebar.selectbox("Chọn Thiết Bị", equipment_list)
        
        # Refresh button
        if st.sidebar.button("Làm Mới Dữ Liệu"):
            self.agent.process_equipment(selected_equipment)
        
        # Process all button
        if st.sidebar.button("Xử Lý Tất Cả Thiết Bị"):
            with st.spinner("Đang xử lý tất cả thiết bị..."):
                self.agent.process_all_equipment()
            st.success("Đã xử lý tất cả thiết bị!")
        
        # Main content area with tabs
        tab1, tab2, tab3 = st.tabs(["Trạng Thái Thiết Bị", "Khuyến Nghị Bảo Trì", "Tổng Quan Hệ Thống"])
        
        with tab1:
            self._render_equipment_status(selected_equipment)
        
        with tab2:
            self._render_maintenance_recommendations(selected_equipment)
        
        with tab3:
            self._render_system_overview()
    
    def _render_equipment_status(self, equipment_id: str):
        """Render the equipment status tab."""
        st.header(f"Trạng thái cho {equipment_id}")
        
        # Get equipment details
        details = self.agent.get_equipment_details(equipment_id)
        summary = details["summary"]
        
        # Create columns for metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Use valid delta_color values: 'normal', 'inverse', or 'off'
            # Map the status to a valid Streamlit delta_color
            status_delta_mapping = {
                "low": "normal",  # green in Streamlit
                "medium": "normal",
                "high": "inverse",  # red in Streamlit
                "critical": "inverse",
                "Unknown": "off"  # neutral in Streamlit
            }
            
            status_names = {
                "low": "Thấp",
                "medium": "Trung bình",
                "high": "Cao",
                "critical": "Nguy cấp",
                "Unknown": "Không xác định"
            }
            
            # Display the status with appropriate delta color
            st.metric("Trạng thái", status_names.get(summary["status"], "Không xác định"),
                      delta=" ",  # Need a non-empty delta to show the color
                      delta_color=status_delta_mapping.get(summary["status"], "off"))
            
            # Use HTML to display the status with custom color
            status_color = {
                "low": "green",
                "medium": "orange",
                "high": "red",
                "critical": "darkred",
                "Unknown": "gray"
            }
            st.markdown(f"<span style='color:{status_color.get(summary['status'], 'gray')};'>{status_names.get(summary['status'], 'KHÔNG XÁC ĐỊNH')}</span>", 
                       unsafe_allow_html=True)
        
        with col2:
            st.metric("% Bất thường", f"{summary['anomaly_percentage']:.2f}%")
        
        with col3:
            st.metric("Ngày từ lần bảo trì cuối", f"{summary['days_since_maintenance']:.0f}")
        
        with col4:
            st.metric("Tổng số đọc", summary["total_readings"])
        
        # Create sensor data plots
        st.subheader("Đọc dữ liệu cảm biến")
        data = pd.DataFrame(details["data"])
        
        # Convert timestamp to datetime if needed
        if 'timestamp' in data.columns and not pd.api.types.is_datetime64_any_dtype(data['timestamp']):
            data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(data, x='timestamp', y=['temperature', 'pressure'], 
                         title='Nhiệt độ & Áp suất')
            fig.update_layout(xaxis_title="Thời gian", yaxis_title="Giá trị")
            st.plotly_chart(fig, use_container_width=True)
            
            fig = px.line(data, x='timestamp', y='vibration', 
                         title='Độ rung', color=data['is_anomaly'].astype(str))
            fig.update_layout(xaxis_title="Thời gian", yaxis_title="Giá trị")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(data, x='timestamp', y=['flow_rate', 'power_consumption'], 
                         title='Lưu lượng & Tiêu thụ điện')
            fig.update_layout(xaxis_title="Thời gian", yaxis_title="Giá trị")
            st.plotly_chart(fig, use_container_width=True)
            
            fig = px.scatter(data, x='vibration', y='temperature', 
                            color=data['is_anomaly'].astype(str),
                            title='Độ rung và Nhiệt độ')
            fig.update_layout(xaxis_title="Độ rung", yaxis_title="Nhiệt độ")
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_maintenance_recommendations(self, equipment_id: str):
        """Render the maintenance recommendations tab."""
        st.header("Khuyến Nghị Bảo Trì")
        
        # Get recommendation for selected equipment
        recommendation = self.agent.maintenance_recommendations.get(equipment_id, {})
        
        if not recommendation:
            st.info(f"Không có khuyến nghị bảo trì cho {equipment_id}. Hãy chạy phân tích trước.")
            return
        
        # Create expandable sections for recommendations
        with st.expander("Phân Tích Vấn Đề", expanded=True):
            st.subheader("Vấn Đề Được Xác Định")
            st.write(recommendation.get("issue", "Không xác định được vấn đề cụ thể"))
            
            st.subheader("Mức Độ Nghiêm Trọng")
            severity = recommendation.get("severity", "low")
            severity_color = {
                "low": "green",
                "medium": "orange",
                "high": "red",
                "critical": "darkred"
            }
            severity_names = {
                "low": "THẤP",
                "medium": "TRUNG BÌNH",
                "high": "CAO",
                "critical": "NGUY CẤP"
            }
            st.markdown(f"<h4 style='color:{severity_color.get(severity, 'gray')}'>{severity_names.get(severity, 'KHÔNG XÁC ĐỊNH')}</h4>", 
                       unsafe_allow_html=True)
            
            st.subheader("Hậu Quả Tiềm Ẩn")
            st.write(recommendation.get("consequences", "Không xác định"))
        
        with st.expander("Hành Động Bảo Trì", expanded=True):
            st.subheader("Hành Động Khuyến Nghị")
            st.write(recommendation.get("recommendation", "Không có khuyến nghị cụ thể"))
            
            st.subheader("Thời Gian Dừng Máy Ước Tính")
            st.write(f"{recommendation.get('estimated_downtime_hours', 'Không xác định')} giờ")
            
            st.subheader("Phụ Tùng Cần Thiết")
            parts = recommendation.get("parts_needed", [])
            if parts:
                for part in parts:
                    st.write(f"- {part}")
            else:
                st.write("Không có phụ tùng cụ thể được liệt kê")
        
        # Add a scheduling option
        st.subheader("Lên Lịch Bảo Trì")
        maintenance_date = st.date_input(
            "Chọn ngày bảo trì", 
            value=datetime.now() + timedelta(days=1)
        )
        maintenance_team = st.selectbox(
            "Chỉ định đội bảo trì",
            ["Đội Alpha", "Đội Beta", "Đội Gamma", "Nhà thầu bên ngoài"]
        )
        
        if st.button("Lên Lịch Bảo Trì"):
            st.success(f"Bảo trì cho {equipment_id} được lên lịch vào ngày {maintenance_date} với {maintenance_team}")
    
    def _render_system_overview(self):
        """Render the system overview tab."""
        st.header("Tổng Quan Hệ Thống")
        
        # Create status summary
        status_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0, "Unknown": 0}
        for equipment, status in self.agent.equipment_status.items():
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Dịch tên trạng thái để hiển thị trên biểu đồ
        status_names = {
            "low": "Thấp",
            "medium": "Trung bình", 
            "high": "Cao", 
            "critical": "Nguy cấp", 
            "Unknown": "Không xác định"
        }
        
        # Create pie chart for status
        fig = go.Figure(data=[go.Pie(
            labels=[status_names.get(key, key) for key in status_counts.keys()],
            values=list(status_counts.values()),
            hole=.3,
            marker=dict(colors=['green', 'orange', 'red', 'darkred', 'gray'])
        )])
        fig.update_layout(title_text="Phân Bố Trạng Thái Thiết Bị")
        st.plotly_chart(fig, use_container_width=True)
        
        # Show all equipment status in a table
        st.subheader("Trạng Thái Tất Cả Thiết Bị")
        
        equipment_data = []
        for equipment_id, status in self.agent.equipment_status.items():
            recommendation = self.agent.maintenance_recommendations.get(equipment_id, {})
            equipment_data.append({
                "Mã Thiết Bị": equipment_id,
                "Trạng Thái": status_names.get(status, status),
                "Vấn Đề": recommendation.get("issue", "Không xác định"),
                "Hành Động Khuyến Nghị": recommendation.get("recommendation", "Không có khuyến nghị")[:100] + "..." 
                                     if recommendation.get("recommendation") and len(recommendation.get("recommendation")) > 100 
                                     else recommendation.get("recommendation", "Không có khuyến nghị"),
                "Thời Gian Ngừng (giờ)": recommendation.get("estimated_downtime_hours", "Không xác định")
            })
        
        df = pd.DataFrame(equipment_data)
        
        # Color-code the table based on status
        def color_status(val):
            status_to_code = {
                'Thấp': 'low',
                'Trung bình': 'medium',
                'Cao': 'high',
                'Nguy cấp': 'critical',
                'Không xác định': 'Unknown'
            }
            status_code = status_to_code.get(val, val)
            
            colors = {
                'low': 'background-color: #c6efce',
                'medium': 'background-color: #ffeb9c',
                'high': 'background-color: #ffc7ce',
                'critical': 'background-color: #9c0006; color: white',
                'Unknown': 'background-color: #d9d9d9'
            }
            return colors.get(status_code, '')
        
        st.dataframe(df.style.applymap(color_status, subset=['Trạng Thái']))
        
        # Maintenance plan if available
        if hasattr(self.agent, 'maintenance_plan') and self.agent.maintenance_plan:
            st.subheader("Kế Hoạch Bảo Trì")
            plan = self.agent.maintenance_plan
            
            st.write(f"**Lịch trình:** {plan.get('schedule', 'Không có thông tin')}")
            st.write(f"**Lý do:** {plan.get('justification', 'Không có thông tin')}")
            st.write(f"**Tổng thời gian ngừng hoạt động:** {plan.get('total_downtime_hours', 'Không xác định')} giờ")
            st.write(f"**Yêu cầu nhân sự:** {plan.get('crew_requirements', 'Không có thông tin cụ thể')}")
            
            st.write("**Danh sách phụ tùng:**")
            for part in plan.get('parts_list', ['Không có thông tin']):
                st.write(f"- {part}")
