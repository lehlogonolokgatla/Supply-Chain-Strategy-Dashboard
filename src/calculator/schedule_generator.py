# src/calculator/schedule_generator.py
from typing import Dict
import datetime


def generate_schedules(solution: Dict, road_network: Dict) -> Dict:
    schedules = {}
    start_time_obj = datetime.datetime.strptime("07:00", "%H:%M")

    for truck_id, route_data in solution.get('routes', {}).items():
        schedule, current_time = [], start_time_obj
        route_nodes = route_data['route']

        for i, node_id in enumerate(route_nodes):
            arrival_time = current_time
            activity = "Start/End Depot" if i == 0 or i == len(route_nodes) - 1 else "Deliver"
            service_time = 0 if activity == "Start/End Depot" else 20
            departure_time = arrival_time + datetime.timedelta(minutes=service_time)

            schedule.append({
                "Stop": i + 1, "Node ID": node_id, "Activity": activity,
                "Arrival": arrival_time.strftime("%H:%M"), "Departure": departure_time.strftime("%H:%M"),
            })

            if i < len(route_nodes) - 1:
                next_node_id = route_nodes[i + 1]
                travel_minutes = road_network.get(node_id, {}).get(next_node_id, {}).get('time', 0)
                current_time = departure_time + datetime.timedelta(minutes=travel_minutes)

        schedules[truck_id] = schedule
    return schedules