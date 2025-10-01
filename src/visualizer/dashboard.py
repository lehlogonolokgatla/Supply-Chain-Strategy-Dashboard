# src/visualizer/dashboard.py
import streamlit as st
import pandas as pd
from typing import Dict, List
from streamlit_folium import st_folium
from src.visualizer.map_plotter import MapPlotter
from src.models.data_models import Farm, Market, Truck

def create_transport_dashboard(
    solution: Dict, costs: Dict, schedules: Dict,
    farms: List[Farm], markets: List[Market], trucks: List[Truck]
):
    if solution.get("error"):
        st.error(f"Optimization Failed: {solution['error']}")
        return

    summary = costs.get('summary', {})
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cost", f"${summary.get('total_overall_cost', 0):,.2f}")
    col2.metric("Total Distance", f"{solution.get('total_distance', 0):,.2f} km")
    col3.metric("Trucks Utilized", f"{len(solution.get('routes', {}))}")
    col4.metric("Total Load Delivered", f"{solution.get('total_load', 0):,.0f} kg")

    st.header("🗺️ Optimized Routes Map")
    map_plotter = MapPlotter(farms, markets, trucks)
    map_plotter.add_markers()
    map_plotter.plot_routes(solution)
    st_folium(map_plotter.map, width=None, height=500)

    st.header("🌍 Sustainability Insights")
    total_co2 = 0
    truck_map = {t.id: t for t in trucks}
    for truck_id, route_data in solution.get('routes', {}).items():
        truck = truck_map.get(truck_id)
        if truck:
            distance_km = route_data['distance_m'] / 100
            total_co2 += distance_km * truck.co2_emissions_g_per_km
    st.metric("Estimated Carbon Footprint", f"{total_co2 / 1000:,.2f} kg CO₂")

    st.header("📊 Performance Breakdown")
    st.subheader("Per-Truck Performance")
    performance_data = []
    active_trucks_map = {t.id: t for t in trucks if t.id in solution.get('routes', {})}
    for truck_id, route_data in solution.get('routes', {}).items():
        truck_obj = active_trucks_map.get(truck_id)
        if truck_obj:
            utilization = (route_data['load_kg'] / truck_obj.capacity_weight) * 100
            performance_data.append({
                "Truck ID": truck_id,
                "Number of Stops": len(route_data['route']) - 2,
                "Route Distance (km)": round(route_data['distance_m'] / 100, 2),
                "Total Load (kg)": route_data['load_kg'],
                "Capacity Utilization (%)": round(utilization, 2),
                "Total Cost ($)": round(costs.get(truck_id, {}).get('total_cost', 0), 2),
                "Cost per Km ($)": round(costs.get(truck_id, {}).get('cost_per_km', 0), 2),
            })
    if performance_data: st.dataframe(pd.DataFrame(performance_data))
    else: st.info("No routes generated.")

    tab1, tab2 = st.tabs(["Cost Analysis", "Delivery Schedules"])
    with tab1:
        st.subheader("Overall Cost Drivers")
        cost_data = {
            "Cost Type": ["Fuel", "Maintenance", "Driver Wages"],
            "Amount ($)": [
                summary.get('total_fuel_cost', 0), summary.get('total_maintenance_cost', 0),
                summary.get('total_driver_cost', 0),
            ]
        }
        cost_df = pd.DataFrame(cost_data).set_index("Cost Type")
        st.bar_chart(cost_df)
    with tab2:
        st.subheader("Schedules per Truck")
        if not schedules: st.warning("No schedules generated.")
        for truck_id, schedule_data in schedules.items():
            with st.expander(f"View schedule for {truck_id}"):
                st.dataframe(pd.DataFrame(schedule_data))