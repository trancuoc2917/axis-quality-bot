import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="Axis Data Quality Bot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Axis Data Quality Bot")
st.markdown("**Professional Trajectory Data Quality Platform**")

API_URL = "http://127.0.0.1:8000"

with st.sidebar:
    st.header("📤 Upload Dữ Liệu")
    uploaded_files = st.file_uploader(
        "Chọn một hoặc nhiều file JSON", 
        type=["json"], 
        accept_multiple_files=True
    )
    
    mode = st.selectbox("Chế độ kiểm tra", ["strict", "normal", "loose"], index=1)
    st.divider()
    st.success("✅ Hệ thống sẵn sàng hoạt động")
    st.caption("Axis Bot v3.2 Final")

if uploaded_files:
    all_results = []
    for uploaded_file in uploaded_files:
        try:
            data = json.load(uploaded_file)
            trajectory = data.get("trajectory") or data.get("steps") or data

            with st.spinner(f"Phân tích {uploaded_file.name}..."):
                resp = requests.post(f"{API_URL}/check", json={
                    "trajectory": trajectory,
                    "mode": mode,
                    "filename": uploaded_file.name
                })
                result = resp.json()
                result["filename"] = uploaded_file.name
                all_results.append(result)
        except Exception as e:
            st.error(f"Lỗi {uploaded_file.name}: {str(e)}")

    if all_results:
        st.success(f"✅ Đã phân tích xong {len(all_results)} file!")

        for result in all_results:
            score = result["score"]
            st.subheader(f"📄 {result['filename']}")

            col1, col2 = st.columns([2, 1])
            with col1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=score,
                    title={"text": "Quality Score"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#00ff88"},
                        'steps': [
                            {'range': [0, 60], 'color': "#ff4d4d"},
                            {'range': [60, 85], 'color': "#ffcc00"},
                            {'range': [85, 100], 'color': "#00ff88"}
                        ]
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.metric("Điểm số", f"{score}/100")
                for k, v in result.get("metrics", {}).items():
                    st.metric(k.replace("_", " ").title(), v)

            st.divider()

        # Tải báo cáo
        st.download_button(
            "📥 Tải toàn bộ báo cáo",
            json.dumps({"reports": all_results}, indent=2, ensure_ascii=False),
            f"axis_full_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )

else:
    st.info("👈 Upload file JSON từ sidebar bên trái để bắt đầu phân tích")

st.divider()
st.subheader("📜 Lịch sử kiểm tra")
try:
    hist = requests.get(f"{API_URL}/history?limit=15").json()
    if hist:
        df = pd.DataFrame(hist)
        df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%d/%m/%Y %H:%M")
        st.dataframe(df[["timestamp", "filename", "score", "mode"]], use_container_width=True)
except:
    st.caption("Chưa có dữ liệu lịch sử.")