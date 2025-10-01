# src/visualizer/map_plotter.py
import folium
from typing import Dict, List
from src.models.data_models import Farm, Market, Truck


class MapPlotter:
    def __init__(self, farms: List[Farm], markets: List[Market], trucks: List[Truck]):
        self.all_locations = {loc.id: loc for loc in farms + markets}
        self.truck_depots = {t.id: t.home_depot_id for t in trucks}
        self.map = folium.Map(location=[0, 0], zoom_start=2)

    def add_markers(self):
        for loc_id, loc in self.all_locations.items():
            is_depot = any(depot_id == loc_id for depot_id in self.truck_depots.values())
            if isinstance(loc, Farm) or is_depot:
                popup, icon = f"Depot/Farm: {loc.id}", folium.Icon(color='green', icon='home')
            else:
                popup, icon = f"Market: {loc.id}<br>Demand: {loc.demand_weight} kg", folium.Icon(color='blue',
                                                                                                 icon='shopping-cart')
            folium.Marker(location=[loc.latitude, loc.longitude], popup=popup, icon=icon).add_to(self.map)

    def plot_routes(self, solution: Dict):
        colors = ['red', 'purple', 'orange', 'darkred', 'cadetblue', 'darkgreen']
        color_index, all_route_points = 0, []

        for truck_id, route_data in solution.get('routes', {}).items():
            route_coords = []
            for node_id in route_data['route']:
                loc = self.all_locations.get(node_id)
                if loc:
                    coords = [loc.latitude, loc.longitude]
                    route_coords.append(coords)
                    all_route_points.append(coords)

            if route_coords:
                folium.PolyLine(
                    locations=route_coords, color=colors[color_index % len(colors)], weight=4,
                    opacity=0.8, tooltip=f"{truck_id} | Distance: {route_data['distance_m'] / 100:.2f} km"
                ).add_to(self.map)
                color_index += 1

        if all_route_points:
            self.map.fit_bounds(all_route_points, padding=(20, 20))