import json
import networkx as nx

f=open('Input data/level0.json')
data=json.load(f)

#list that stores neighbour distance
distance_neigh=[]
dist=[]
for val in data['neighbourhoods']:
    for i in data['neighbourhoods'][val]['distances']:
        dist.append(i)
    distance_neigh.append(dist)
    dist=[]

#list that stores restaurant distance
restaurants=[]
for i in data['restaurants']['r0']['neighbourhood_distance']:
    restaurants.append(i)

#graph
#make restaurant as 20 location
G=nx.Graph()

for i in range(0,20,1):
    G.add_edge(i+1,0,length=restaurants[i])
    G.add_edge(0,i+1,length=restaurants[i])

for i in range(0,20,1):
    for j in range(i+1,20,1):
        G.add_edge(i+1,j+1,length=distance_neigh[i][j])

# Use networkx function for TSP
tsp_path = nx.approximation.traveling_salesman_problem(G,cycle=True)
starting_node = 20
if starting_node in tsp_path:
    tsp_path.remove(20)
    tsp_path = [starting_node] + tsp_path
    tsp_path[-1]=20
print(f"TSP path: {tsp_path}")

#creating output file
tsp=["r0"]
for i in tsp_path:
    if i!=20:
        tsp.append("n"+str(i))
tsp.append("r0")
answer={"v0":{"path":tsp}}

with open("level0_output.json", "w") as outfile: 
    json.dump(answer, outfile)


