import sys
import json 

def solve_knapsack(orders, distances, capacity):

    n = len(orders)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if orders[i - 1] <= w:
                dp[i][w] = max(distances[i - 1] + dp[i - 1][w - orders[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    selected_orders = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_orders.append(i - 1)
            w -= orders[i - 1]

    return selected_orders


def solve_tsp(distances):
    n = len(distances)
    visited = [False] * n
    path = [0]
    visited[0] = True

    for _ in range(n - 1):
        min_dist = sys.maxsize
        nearest_city = -1
        current_city = path[-1]

        for city in range(n):
            if not visited[city] and distances[current_city][city] < min_dist:
                min_dist = distances[current_city][city]
                nearest_city = city

        path.append(nearest_city)
        visited[nearest_city] = True

    path.append(0)  
    return path

def solve_neighborhood_knapsack(neighborhood_data, vehicle_capacity):
    orders = neighborhood_data['order_quantity']
    distances = neighborhood_data['distances']
    selected_orders = solve_knapsack(orders, distances, vehicle_capacity)
    return selected_orders

def solve_vehicle_route(selected_orders):
    vehicle_route = solve_tsp(selected_orders)
    return vehicle_route

def solve_all_neighborhoods(data):
    vehicle_capacity = data['vehicles']['v0']['capacity']
    neighborhoods = data['neighbourhoods']
    vehicle_route = []
    
    for neighborhood_id, neighborhood_data in neighborhoods.items():
        selected_orders = solve_neighborhood_knapsack(neighborhood_data, vehicle_capacity)
        neighborhood_vehicle_route = solve_vehicle_route(selected_orders)
        vehicle_route.append(neighborhood_vehicle_route)
    
    return vehicle_route


f = open('Input data/level1a.json')
data = json.load(f)
final_vehicle_route = solve_all_neighborhoods(data)

print(final_vehicle_route)
def format_output(vehicle_routes):
    formatted_output = {"v0": {}}
    for i, route in enumerate(vehicle_routes, start=1):
        formatted_output["v0"]["path" + str(i)] = route
    return formatted_output

"""
output = format_output(final_vehicle_routes)
output_json = json.dumps(output, indent=2)
print(output_json)
"""


