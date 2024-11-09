from typing import List, Dict

class OptimizationAgent:
    def __init__(self):
        # Define transport options with estimated costs per kilometer and speeds in km/h
        self.transport_options = {
            "walking": {"cost_per_km": 0, "speed_kmh": 5},
            "public_transport": {"cost_per_km": 0.5, "speed_kmh": 20},
            "taxi": {"cost_per_km": 1.5, "speed_kmh": 40}
        }

    def optimize_route(self, itinerary: List[Dict], budget: float) -> List[Dict]:
        """
        Optimizes the itinerary based on user budget by choosing transport modes
        to balance cost and travel time.
        """
        total_cost = 0
        optimized_itinerary = []

        for i, stop in enumerate(itinerary):
            # Calculate the travel method based on remaining budget and distance
            if i == 0:
                # First stop - start from initial point, no travel cost
                stop['transport'] = 'walking'  # Default transport mode to the first attraction
            else:
                previous_stop = optimized_itinerary[i - 1]
                distance_km = self.estimate_distance(previous_stop, stop)

                # Determine the optimal transport based on budget and time constraints
                selected_transport = self.select_transport(distance_km, budget - total_cost)
                travel_cost = self.calculate_travel_cost(distance_km, selected_transport)

                # Update total cost and assign the selected transport mode
                total_cost += travel_cost
                stop['transport'] = selected_transport
                stop['travel_cost'] = travel_cost
                stop['distance_from_previous'] = distance_km

            # Add the optimized stop to the itinerary
            optimized_itinerary.append(stop)

        return optimized_itinerary

    def estimate_distance(self, start: Dict, end: Dict) -> float:
        """
        Estimates the distance in kilometers between two points.
        For simplicity, a fixed average distance is assumed here.
        In real applications, use geolocation APIs for accurate distance.
        """
        # Example: Assume an average distance between stops for demo purposes
        average_distance_km = 2  # Placeholder; replace with real distance if available
        return average_distance_km

    def select_transport(self, distance_km: float, remaining_budget: float) -> str:
        """
        Selects the optimal transport mode based on the distance and remaining budget.
        """
        if distance_km <= 1:  # Short distances are suitable for walking
            return "walking"
        
        # Check transport options by cost, preferring faster options within budget
        for transport_mode, option in sorted(self.transport_options.items(), key=lambda x: x[1]['cost_per_km']):
            estimated_cost = distance_km * option['cost_per_km']
            if estimated_cost <= remaining_budget:
                return transport_mode
        
        # Default to the cheapest option if budget is limited
        return "walking"

    def calculate_travel_cost(self, distance_km: float, transport_mode: str) -> float:
        """
        Calculates the travel cost for a given distance and transport mode.
        """
        cost_per_km = self.transport_options[transport_mode]["cost_per_km"]
        return distance_km * cost_per_km
