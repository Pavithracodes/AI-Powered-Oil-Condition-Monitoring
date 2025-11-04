import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from supabase import create_client
import os
from dotenv import load_dotenv
import joblib

st.set_page_config(page_title='Oil Condition Monitoring (AI-Enhanced)', layout='wide')

# Load .env
load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    st.error('❌ Missing SUPABASE_URL or SUPABASE_ANON_KEY in .env')
    st.stop()

client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Load ML model
@st.cache_resource
def load_model():
    return joblib.load("oil_health_model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error(f"⚠️ Could not load ML model: {e}")
    st.stop()

# Sidebar Controls
st.sidebar.header('Controls')
vehicle_filter = st.sidebar.selectbox('Vehicle', ['all', 'truck-1', 'truck-2'])
rows = st.sidebar.slider('Rows to show', 10, 500, 100)
refresh_rate = st.sidebar.selectbox('Refresh every (s)', [2, 5, 10, 15], index=1)

# Fetch latest readings
@st.cache_data(ttl=5)
def get_latest_readings(limit=100, vehicle=None):
    query = client.table('sensor_readings').select('*').order('ts', desc=True).limit(limit)
    if vehicle and vehicle != 'all':
        query = query.eq('vehicle_id', vehicle)
    resp = query.execute()
    df = pd.DataFrame(resp.data) if resp.data else pd.DataFrame()
    if df.empty:
        return df
    df['ts'] = pd.to_datetime(df['ts'])
    return df.sort_values('ts')

# Fetch latest alerts
def get_latest_alerts(limit=20):
    resp = client.table('alerts').select('*').order('ts', desc=True).limit(limit).execute()
    alert_df = pd.DataFrame(resp.data) if resp.data else pd.DataFrame()
    return alert_df

# ---------------------------
# Main Dashboard
# ---------------------------
st.title("🧠 AI-Powered Oil Condition Monitoring Dashboard")

df = get_latest_readings(limit=rows, vehicle=vehicle_filter)
alert_df = get_latest_alerts()

if not df.empty:
    # ML Predictions
    X = df[["oil_temp_c", "viscosity_cp", "pressure_kpa"]]
    df["predicted_status"] = model.predict(X)
    probs = model.predict_proba(X)
    df["critical_prob"] = probs[:, list(model.classes_).index("critical")] * 100

    # Display Data
    st.subheader("Live Sensor Data + AI Predictions")
    st.dataframe(df[["ts", "vehicle_id", "oil_temp_c", "viscosity_cp", "pressure_kpa", "predicted_status", "critical_prob"]])

    # Probability Bars
    st.markdown("### 🔥 Predicted Failure Probability")
    for i, row in df.tail(10).iterrows():
        prob = row["critical_prob"]
        color = "green" if prob < 30 else "orange" if prob < 70 else "red"
        st.markdown(
            f"<div style='margin:5px 0;'>🚗 {row['vehicle_id']} — <b>{prob:.1f}%</b> chance of oil failure</div>"
            f"<div style='background-color:#ddd;width:100%;height:12px;border-radius:10px;'>"
            f"<div style='width:{prob:.1f}%;background-color:{color};height:12px;border-radius:10px;'></div></div>",
            unsafe_allow_html=True
        )

    # Pie Chart of Predictions
    st.subheader("🔍 Oil Health Status Distribution")
    counts = df["predicted_status"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", colors=["green", "orange", "red"])
    ax.set_title("Predicted Oil Health")
    st.pyplot(fig)
else:
    st.info("Waiting for live sensor data...")

# Alerts
if not alert_df.empty:
    st.subheader("⚠️ Latest Alerts")
    st.table(alert_df[['ts', 'vehicle_id', 'severity', 'message']])
else:
    st.write("No alerts yet.")


