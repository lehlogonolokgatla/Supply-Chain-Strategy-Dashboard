# src/calculator/cost_calculator.py
from typing import Dict, List
from src.data_manager.config_manager import ConfigManager
from src.models.data_models import Truck


def calculate_all_costs(solution: Dict, trucks: List[Truck], road_network: Dict, config: ConfigManager) -> Dict:
    all_costs = {}
    truck_map = {t.id: t for t in trucks}

    total_cost, total_fuel_cost, total_maintenance_cost, total_driver_cost = 0.0, 0.0, 0.0, 0.0

    for truck_id, route_data in solution.get('routes', {}).items():
        truck = truck_map.get(truck_id)
        if not truck: continue

        route_time_minutes = 0
        for i in range(len(route_data['route']) - 1):
            from_node, to_node = route_data['route'][i], route_data['route'][i + 1]
            route_time_minutes += road_network.get(from_node, {}).get(to_node, {}).get('time', 0)

        distance_km = route_data['distance_m'] / 100
        fuel_cost = (distance_km / 100) * truck.avg_fuel_consumption_L_per_100km * config.get_param('variable_costs',
                                                                                                    'fuel_cost_per_liter')
        maintenance_cost = distance_km * config.get_param('variable_costs', 'maintenance_cost_per_km')
        driver_cost = (route_time_minutes / 60) * config.get_param('variable_costs', 'driver_wage_per_hour')

        route_total_cost = fuel_cost + maintenance_cost + driver_cost
        total_cost += route_total_cost
        total_fuel_cost += fuel_cost
        total_maintenance_cost += maintenance_cost
        total_driver_cost += driver_cost

        all_costs[truck_id] = {
            'total_cost': route_total_cost, 'fuel_cost': fuel_cost, 'maintenance_cost': maintenance_cost,
            'driver_cost': driver_cost, 'cost_per_km': route_total_cost / distance_km if distance_km > 0 else 0
        }

    all_costs['summary'] = {
        'total_overall_cost': total_cost, 'total_fuel_cost': total_fuel_cost,
        'total_maintenance_cost': total_maintenance_cost, 'total_driver_cost': total_driver_cost,
    }
    return all_costs