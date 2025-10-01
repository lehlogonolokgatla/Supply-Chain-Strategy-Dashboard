# src/models/data_models.py
from pydantic import BaseModel, Field
from typing import List, Dict

class Farm(BaseModel):
    id: str
    latitude: float
    longitude: float
    inventory_weight: float = Field(..., gt=0)
    loading_time_window: str

class Market(BaseModel):
    id: str
    latitude: float
    longitude: float
    demand_weight: float = Field(..., gt=0)
    service_time_window: str
    demand_variability: float
    lead_time_days: int

class Truck(BaseModel):
    id: str
    capacity_weight: float = Field(..., gt=0)
    capacity_volume: float = Field(..., gt=0)
    fuel_type: str
    avg_fuel_consumption_L_per_100km: float = Field(..., gt=0)
    driver_hours_limit: float = Field(..., gt=0)
    home_depot_id: str
    co2_emissions_g_per_km: float

class RoadNetwork(BaseModel):
    matrix: Dict[str, Dict[str, Dict[str, float]]]