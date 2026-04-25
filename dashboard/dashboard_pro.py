import streamlit as st
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="AI Traffic Dashboard", layout="wide")

st.title("🚦 AI Traffic Control Dashboard")

# 🔄 Auto refresh every 10 sec
st_autorefresh(interval=10000, key="refresh")

# ---------------- API CALL ----------------
try:
    response = requests.get("http://127.0.0.1:5000/traffic")
    data = response.json()

    queue = data.get("queue", [0, 0, 0, 0])
    signal = data.get("signal", 0)
    throughput = data.get("throughput", 0)
    delay = data.get("delay", 0)

    # ---------------- TOP METRICS ----------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🚗 Total Vehicles", sum(queue))
    col2.metric("🚦 Active Signal", f"Lane {signal}")
    col3.metric("📈 Throughput", throughput)
    col4.metric("⏱ Delay", round(delay, 2))

    st.markdown("---")

    # ---------------- QUEUE CHART ----------------
    st.subheader("🚗 Lane-wise Queue")

    df = pd.DataFrame({
        "Lane": ["Lane 0", "Lane 1", "Lane 2", "Lane 3"],
        "Vehicles": queue
    })

    st.bar_chart(df.set_index("Lane"))

    # ---------------- SIGNAL STATUS ----------------
    st.subheader("🚦 Signal Status")

    cols = st.columns(4)

    for i in range(4):
        if i == signal:
            cols[i].success(f"🟢 Lane {i}")
        else:
            cols[i].error(f"🔴 Lane {i}")

    st.markdown("---")

    # ---------------- HISTORY GRAPH ----------------
    st.subheader("📊 Traffic Trend")

    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append(sum(queue))

    hist_df = pd.DataFrame(st.session_state.history, columns=["Total Queue"])

    st.line_chart(hist_df)

except Exception as e:
    st.error(f"⚠️ API Error: {e}")