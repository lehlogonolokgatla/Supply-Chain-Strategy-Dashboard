# src/pages/2_Transportation_Optimizer.py
import streamlit as st
from src.data_manager import input_loader, config_manager
from src.optimizer.vrp_solver import VRPSolver
from src.calculator import cost_calculator, schedule_generator
from src.visualizer.dashboard import create_transport_dashboard
from src.models.data_models import Farm, Market, Truck, RoadNetwork

st.title("🚚 Transportation & Routing Optimization")


def get_data():
    if st.session_state.get('data_loaded', False):
        st.info("Using custom data uploaded from the Home page.")
        farms = [Farm(**row) for _, row in st.session_state['farms_df'].iterrows()]
        markets = [Market(**row) for _, row in st.session_state['markets_df'].iterrows()]
        trucks = [Truck(**row) for _, row in st.session_state['trucks_df'].iterrows()]
        road_network = RoadNetwork(matrix=st.session_state['network_dict'])
    else:
        st.info("Using default sample data.")
        farms = input_loader.load_farms('data/farms.csv')
        markets = input_loader.load_markets('data/markets.csv')
        trucks = input_loader.load_trucks('data/trucks.csv')
        road_network = input_loader.load_road_network('data/road_network_matrix.json')
    config = config_manager.ConfigManager('data/config.json')
    return farms, markets, trucks, road_network, config


farms, markets, trucks, road_network, config = get_data()


@st.cache_data
def run_optimization(_trucks, _markets, _road_network, _config, active_truck_ids, fuel_cost_per_liter):
    print("--- RUNNING TRANSPORTATION OPTIMIZATION ---")
    active_trucks = [t for t in _trucks if t.id in active_truck_ids]

    _config.config['variable_costs']['fuel_cost_per_liter'] = fuel_cost_per_liter

    if not active_trucks: return {"error": "No trucks selected."}, {}, {}

    solver = VRPSolver(markets=_markets, trucks=active_trucks, road_network=_road_network)
    solution = solver.solve()

    costs, schedules = {}, {}
    if not solution.get("error"):
        costs = cost_calculator.calculate_all_costs(solution, active_trucks, _road_network.matrix, _config)
        schedules = schedule_generator.generate_schedules(solution, _road_network.matrix)
    return solution, costs, schedules


st.sidebar.header("Scenario Controls")
all_truck_ids = [t.id for t in trucks]
active_trucks_input = st.sidebar.multiselect("Active Trucks", options=all_truck_ids, default=all_truck_ids)
fuel_cost_input = st.sidebar.slider(
    "Fuel Cost per Liter", 0.5, 3.0,
    config.get_param('variable_costs', 'fuel_cost_per_liter'), 0.05
)

solution, costs, schedules = run_optimization(trucks, markets, road_network, config, tuple(active_trucks_input),
                                              fuel_cost_input)

create_transport_dashboard(solution, costs, schedules, farms, markets, trucks)