import streamlit as st
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="AI Traffic Dashboard", layout="centered")

st.title("🚦 AI Traffic Dashboard")

# 🔥 auto refresh (30 sec)
st_autorefresh(interval=30000, key="traffic_refresh")

try:
    response = requests.get("http://127.0.0.1:5000/traffic")
    data = response.json()

    df = pd.DataFrame({
        "Lane": ["Lane 0", "Lane 1", "Lane 2", "Lane 3"],
        "Vehicles": data["queue"]
    })

    st.subheader("🚗 Queue Lengths")
    st.bar_chart(df.set_index("Lane"))

    st.subheader("🚦 Traffic Signal Status")

    for i in range(4):
        if i == data["signal"]:
            st.success(f"🟢 Lane {i} GREEN")
        else:
            st.error(f"🔴 Lane {i} RED")

except Exception as e:
    st.error(f"⚠️ Error: {e}")