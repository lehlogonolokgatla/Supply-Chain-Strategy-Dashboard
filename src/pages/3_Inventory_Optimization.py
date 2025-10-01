# src/pages/3_Inventory_Optimization.py
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm

st.title("📦 Inventory Optimization")
st.markdown("This module helps determine the optimal inventory levels to balance stockout risks and holding costs.")


def get_market_data():
    if st.session_state.get('data_loaded', False):
        st.info("Using custom data uploaded from the Home page.")
        return st.session_state['markets_df']
    else:
        st.info("Using default sample data.")
        try:
            return pd.read_csv('data/markets.csv')
        except FileNotFoundError:
            return None


markets_df = get_market_data()

if markets_df is None:
    st.error("Market data not found. Please upload it or run the data generation script.")
    st.stop()

st.header("Safety Stock & Reorder Point Calculator")
selected_market = st.selectbox("Select a Market/Product to Analyze", options=markets_df['id'])

if selected_market:
    market_data = markets_df[markets_df['id'] == selected_market].iloc[0]
    avg_demand = market_data['demand_weight']
    demand_std_dev = avg_demand * market_data['demand_variability']
    lead_time = market_data['lead_time_days']

    st.subheader(f"Inputs for: {selected_market}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Daily Demand", f"{avg_demand:,.0f} kg")
    col2.metric("Demand Std Dev", f"{demand_std_dev:,.0f} kg")
    col3.metric("Supplier Lead Time", f"{lead_time} days")

    st.subheader("Strategic Decisions")
    service_level = st.slider("Desired Service Level (%)", 80, 100, 95, 1) / 100

    z_score = norm.ppf(service_level)
    safety_stock = z_score * demand_std_dev * np.sqrt(lead_time)
    reorder_point = (avg_demand * lead_time) + safety_stock

    st.subheader("Recommendations")
    col1, col2 = st.columns(2)
    col1.metric("Calculated Safety Stock", f"{safety_stock:,.2f} kg")
    col2.metric("Calculated Reorder Point", f"{reorder_point:,.2f} kg")

    st.success(
        f"**Insight:** To achieve a **{service_level:.0%} service level** for **{selected_market}**, maintain a safety stock of **{safety_stock:,.0f} kg** and reorder when inventory hits **{reorder_point:,.0f} kg**.")