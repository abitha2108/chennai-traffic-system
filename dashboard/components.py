import streamlit as st

def show_signal(signal):
    st.subheader("🚦 Signal Status")

    for i in range(4):
        if i == signal:
            st.success(f"🟢 Lane {i} GREEN")
        else:
            st.error(f"🔴 Lane {i} RED")