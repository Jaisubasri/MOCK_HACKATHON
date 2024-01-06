import json
import networkx as nx

f = open('Input data/level0.json')
data = json.load(f)

# List that stores neighborhood distance
distance_neigh = []
dist = []
for val in data['neighbourhoods']:
    for i in data['neighbourhoods'][val]['distances']:
        dist.append(i)
    distance_neigh.append(dist)
    dist = []

# List that stores restaurant distance
restaurants = []
for i in data['restaurants']['r0']['neighbourhood_distance']:
    restaurants.append(i)

# Graph
# Make restaurant as 20 locations
G = nx.Graph()


for i in range(0, 20, 1):
    for j in range(i + 1, 20, 1):
        G.add_edge(i + 1, j + 1, length=distance_neigh[i][j])

for i in range(0, 20, 1):
    G.add_edge(i + 1, 0, length=restaurants[i])
    G.add_edge(0, i + 1, length=restaurants[i])

# Greedy TSP algorithm
def greedy_tsp(graph, start_node):
    current_node = start_node
    visited_nodes = set([start_node])
    tsp_path = [current_node]

    while len(visited_nodes) < graph.number_of_nodes():
        neighbors = graph.neighbors(current_node)
        next_node = min(neighbors, key=lambda x: graph[current_node][x]['length'] if x not in visited_nodes else float('inf'))
        tsp_path.append(next_node)
        visited_nodes.add(next_node)
        current_node = next_node

    # Return to the starting node
    tsp_path.append(start_node)

    return tsp_path

# Use the greedy TSP algorithm
tsp_path = greedy_tsp(G, start_node=20)

print(f"Greedy TSP path: {tsp_path}")

# Creating output file
tsp = ["r0"]
for i in tsp_path:
    if i != 20:
        tsp.append("n" + str(i))
tsp.append("r0")
answer = {"v0": {"path": tsp}}
print(answer)
with open("level0_output.json", "w") as outfile:
    json.dump(answer, outfile)
