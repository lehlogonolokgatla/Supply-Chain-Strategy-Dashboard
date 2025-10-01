# scripts/generate_dummy_data.py
import pandas as pd
import json
from faker import Faker
import random
import os
import math
from datetime import time

print("--- Starting Dummy Data Generation ---")

# --- Configuration ---
NUM_FARMS = 4
NUM_MARKETS = 12
NUM_TRUCKS = 3
DATA_DIR = 'data'

# --- Setup ---
os.makedirs(DATA_DIR, exist_ok=True)
fake = Faker('en_US')

# --- Helper Functions ---
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points on Earth in kilometers."""
    R = 6371  # Radius of Earth
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# --- Data Generation Functions ---
def generate_farms(num_farms):
    data = []
    for i in range(num_farms):
        start_hour = random.randint(6, 9)
        data.append({
            "id": f"FARM_{i+1:02d}",
            "latitude": float(fake.latitude()),
            "longitude": float(fake.longitude()),
            "inventory_weight": round(random.uniform(2000, 8000), 2),
            "loading_time_window": f"{time(start_hour, 0).strftime('%H:%M')}-{time(start_hour + 4, 0).strftime('%H:%M')}"
        })
    return pd.DataFrame(data)

def generate_markets(num_markets):
    data = []
    for i in range(num_markets):
        start_hour = random.randint(9, 14)
        data.append({
            "id": f"MARKET_{i+1:02d}",
            "latitude": float(fake.latitude()),
            "longitude": float(fake.longitude()),
            "demand_weight": round(random.uniform(500, 2500), 2),
            "service_time_window": f"{time(start_hour, 0).strftime('%H:%M')}-{time(start_hour + 2, 0).strftime('%H:%M')}",
            "demand_variability": round(random.uniform(0.1, 0.4), 2),
            "lead_time_days": random.randint(2, 7)
        })
    return pd.DataFrame(data)

def generate_trucks(num_trucks, depot_ids):
    data = []
    for i in range(num_trucks):
        data.append({
            "id": f"TRUCK_{i+1:02d}",
            "capacity_weight": float(random.choice([8000, 10000, 12000])),
            "capacity_volume": float(random.choice([30, 40, 50])),
            "fuel_type": "Diesel",
            "avg_fuel_consumption_L_per_100km": round(random.uniform(25, 35), 1),
            "driver_hours_limit": 10.0,
            "home_depot_id": random.choice(depot_ids),
            "co2_emissions_g_per_km": round(random.uniform(700, 950), 1)
        })
    return pd.DataFrame(data)

def generate_road_network_matrix(locations_df):
    ids = locations_df['id'].tolist()
    coords = {row['id']: (row['latitude'], row['longitude']) for _, row in locations_df.iterrows()}
    matrix = {}
    for origin_id in ids:
        matrix[origin_id] = {}
        for dest_id in ids:
            if origin_id == dest_id:
                matrix[origin_id][dest_id] = {'distance': 0, 'time': 0}
                continue
            lat1, lon1 = coords[origin_id]
            lat2, lon2 = coords[dest_id]
            distance_km = haversine_distance(lat1, lon1, lat2, lon2) * 1.3
            time_minutes = round((distance_km / random.uniform(50, 70)) * 60)
            matrix[origin_id][dest_id] = {'distance': round(distance_km, 2), 'time': time_minutes}
    return matrix

def generate_config():
    return {
      "variable_costs": {"fuel_cost_per_liter": 1.75, "maintenance_cost_per_km": 0.15, "driver_wage_per_hour": 28.0},
      "fixed_costs": {"vehicle_depreciation_per_day": 50.0, "insurance_per_day": 15.0},
      "optimization_constraints": {"max_driving_hours_per_day": 10, "penalty_late_delivery_per_minute": 5.0}
    }

# --- Main Execution ---
if __name__ == "__main__":
    farms_df = generate_farms(NUM_FARMS)
    farms_df.to_csv(os.path.join(DATA_DIR, 'farms.csv'), index=False)
    print(f"Generated {len(farms_df)} farms -> data/farms.csv")

    markets_df = generate_markets(NUM_MARKETS)
    markets_df.to_csv(os.path.join(DATA_DIR, 'markets.csv'), index=False)
    print(f"Generated {len(markets_df)} markets -> data/markets.csv")

    trucks_df = generate_trucks(NUM_TRUCKS, depot_ids=farms_df['id'].tolist())
    trucks_df.to_csv(os.path.join(DATA_DIR, 'trucks.csv'), index=False)
    print(f"Generated {len(trucks_df)} trucks -> data/trucks.csv")

    all_locations_df = pd.concat([farms_df[['id', 'latitude', 'longitude']], markets_df[['id', 'latitude', 'longitude']]])
    road_network = generate_road_network_matrix(all_locations_df)
    with open(os.path.join(DATA_DIR, 'road_network_matrix.json'), 'w') as f:
        json.dump(road_network, f, indent=4)
    print("Generated road network matrix -> data/road_network_matrix.json")

    config_data = generate_config()
    with open(os.path.join(DATA_DIR, 'config.json'), 'w') as f:
        json.dump(config_data, f, indent=4)
    print("Generated config file -> data/config.json")

    print("--- Dummy Data Generation Complete! ---")