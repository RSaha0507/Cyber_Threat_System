import streamlit as st
import pandas as pd
from alerts.alert_generation_module import generate_alert
from db.mongo_client import threats_collection
from aggregator.fetch_feeds import ingest_threat
from aggregator.otx_live_feed import fetch_and_store_otx_threats
from detection.anomaly_detector import detect_best_anomaly_model
from aggregator.abuseip_feed import fetch_and_store_abuseip_threats
from utils.ip_geo import get_geo_location
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Cyber Threat Dashboard", layout="wide")
st.title("🛡️ Cyber Threat Intelligence & Response System")

# --- Ingest Buttons ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧪 Ingest Simulated Threat"):
        ingest_threat()
        st.success("Simulated threat inserted.")

with col2:
    if st.button("🌐 Fetch Real Threats from OTX"):
        fetch_and_store_otx_threats()
        st.success("Fetched real threat data from AlienVault OTX.")

with col3:
    if st.button("🌐 Fetch AbuseIPDB Threats"):
     fetch_and_store_abuseip_threats()
     st.success("Fetched AbuseIPDB blacklisted IPs.")

# --- Fetch Data from MongoDB ---
threats = list(threats_collection.find().sort("timestamp", -1))
df = pd.DataFrame(threats)

# Drop MongoDB's default ID field
if "_id" in df.columns:
    df.drop("_id", axis=1, inplace=True)

# --- Show Latest Threats ---
st.subheader("📋 Latest Threats")
if not df.empty:
    st.dataframe(df[["timestamp", "ip", "threat_level", "category", "source"]])
else:
    st.info("No threat data available.")

# --- Anomaly Detection ---
anomalies, model_used = detect_best_anomaly_model(df)

st.subheader("🔍 Detected Anomalies")
st.caption(f"🧠 Detection Model Used: {model_used}")
if not anomalies.empty:
    st.dataframe(anomalies[["timestamp", "ip", "threat_level", "category", "source"]])
else:
    st.success("✅ No anomalies detected.")

# 🌍 Geolocation Map of Anomalies
st.subheader("🌍 Geolocation Map of Anomalies")

geo_data = []

for ip in anomalies["ip"].unique():
    geo_info = get_geo_location(ip)
    if geo_info and geo_info["lat"] is not None and geo_info["lon"] is not None:
        geo_data.append({
            "ip": ip,
            "city": geo_info["city"],
            "country": geo_info["country"],
            "lat": geo_info["lat"],
            "lon": geo_info["lon"]
        })

if geo_data:
    map_center = [geo_data[0]['lat'], geo_data[0]['lon']]
    m = folium.Map(location=map_center, zoom_start=2)

    for item in geo_data:
        folium.Marker(
            location=[item["lat"], item["lon"]],
            popup=f"{item['ip']} - {item['city']}, {item['country']}",
            icon=folium.Icon(color="red")
        ).add_to(m)

    st_folium(m, width=700)
else:
    st.info("No valid geolocation data for current anomalies.")


# --- Real-Time Alert Simulation ---
st.subheader("🚨 Real-Time Alert Simulation")

if "alerts" not in st.session_state:
    st.session_state.alerts = []

if st.button("⚡ Generate Simulated Alert"):
    new_alert = generate_alert()
    st.session_state.alerts.append(new_alert.to_dict())
    st.success(f"New alert generated: {new_alert.alert_id}")

if st.session_state.alerts:
    st.dataframe(st.session_state.alerts)
else:
    st.info("No alerts generated yet.")
