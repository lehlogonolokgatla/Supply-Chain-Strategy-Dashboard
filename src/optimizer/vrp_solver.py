# src/optimizer/vrp_solver.py
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
from typing import List, Dict, Any
from src.models.data_models import Market, Truck, RoadNetwork


class VRPSolver:
    def __init__(self, markets: List[Market], trucks: List[Truck], road_network: RoadNetwork):
        self.markets = markets
        self.trucks = trucks
        self.road_network = road_network.matrix
        self._build_data_model()

    def _build_data_model(self):
        self.data = {}
        depot_id = self.trucks[0].home_depot_id

        self.locations = [depot_id] + [m.id for m in self.markets]
        self.location_map = {loc_id: i for i, loc_id in enumerate(self.locations)}
        num_locations = len(self.locations)

        self.data['distance_matrix'] = [[0] * num_locations for _ in range(num_locations)]
        for from_node in self.locations:
            for to_node in self.locations:
                from_idx = self.location_map[from_node]
                to_idx = self.location_map[to_node]
                self.data['distance_matrix'][from_idx][to_idx] = int(
                    self.road_network.get(from_node, {}).get(to_node, {}).get('distance', 0) * 100)

        self.data['demands'] = [0] + [int(m.demand_weight) for m in self.markets]
        self.data['vehicle_capacities'] = [int(t.capacity_weight) for t in self.trucks]
        self.data['num_vehicles'] = len(self.trucks)
        self.data['depot'] = 0

    def solve(self) -> Dict[str, Any]:
        manager = pywrapcp.RoutingIndexManager(len(self.data['distance_matrix']), self.data['num_vehicles'],
                                               self.data['depot'])
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return self.data['demands'][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index, 0, self.data['vehicle_capacities'], True, 'Capacity'
        )

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit.FromSeconds(30)

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            return self._format_solution(manager, routing, solution)
        else:
            return {"error": "No solution found."}

    def _format_solution(self, manager, routing, solution) -> Dict[str, Any]:
        output = {'routes': {}, 'total_distance': 0, 'total_load': 0}
        for vehicle_id in range(self.data['num_vehicles']):
            index = routing.Start(vehicle_id)
            truck_id = self.trucks[vehicle_id].id
            route_nodes, route_distance, route_load = [], 0, 0
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                if node_index != self.data['depot']:
                    route_nodes.append(self.locations[node_index])
                    route_load += self.data['demands'][node_index]
                previous_index, index = index, solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

            if route_nodes:
                output['routes'][truck_id] = {
                    'route': [self.locations[self.data['depot']]] + route_nodes + [self.locations[self.data['depot']]],
                    'distance_m': route_distance, 'load_kg': route_load
                }
                output['total_distance'] += route_distance
                output['total_load'] += route_load

        output['total_distance'] /= 100
        return output