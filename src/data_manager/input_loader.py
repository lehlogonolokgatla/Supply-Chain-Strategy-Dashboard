# src/data_manager/input_loader.py
import pandas as pd
import json
from typing import List
from src.models.data_models import Farm, Market, Truck, RoadNetwork

def load_farms(filepath: str) -> List[Farm]:
    df = pd.read_csv(filepath)
    return [Farm(**row) for row in df.to_dict(orient='records')]

def load_markets(filepath: str) -> List[Market]:
    df = pd.read_csv(filepath)
    return [Market(**row) for row in df.to_dict(orient='records')]

def load_trucks(filepath: str) -> List[Truck]:
    df = pd.read_csv(filepath)
    return [Truck(**row) for row in df.to_dict(orient='records')]

def load_road_network(filepath: str) -> RoadNetwork:
    with open(filepath, 'r') as f:
        data = json.load(f)
    return RoadNetwork(matrix=data)