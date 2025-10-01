# src/1_Home.py
import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide", page_title="OpsDash Home")

st.title("📈 Operations & Strategy Dashboard")
st.markdown("""
Welcome! This tool is designed to turn raw operational data into actionable strategic insights.

**How to use this tool:**
1.  **Use Sample Data:** The dashboard is pre-loaded with sample data. Simply navigate to the pages in the sidebar to see the analysis.
2.  **Upload Your Own Data:** For a custom analysis, use the file uploaders below. The dashboard will automatically use your data once all files are loaded.

---
""")

if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False

st.header("Upload Your Datasets (Optional)")
col1, col2, col3, col4 = st.columns(4)

uploaded_farms = col1.file_uploader("Upload Farms CSV", type="csv")
uploaded_markets = col2.file_uploader("Upload Markets CSV", type="csv")
uploaded_trucks = col3.file_uploader("Upload Trucks CSV", type="csv")
uploaded_network = col4.file_uploader("Upload Road Network JSON", type="json")

if uploaded_farms and uploaded_markets and uploaded_trucks and uploaded_network:
    st.session_state['farms_df'] = pd.read_csv(uploaded_farms)
    st.session_state['markets_df'] = pd.read_csv(uploaded_markets)
    st.session_state['trucks_df'] = pd.read_csv(uploaded_trucks)
    st.session_state['network_dict'] = json.load(uploaded_network)
    st.session_state['data_loaded'] = True
    st.success("Custom data loaded! Navigate to other pages for analysis.")

if st.session_state['data_loaded']:
    st.info("✅ Custom data is loaded and will be used for analysis.")
else:
    st.info("ℹ️ No custom data loaded. Using default sample data.")