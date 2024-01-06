import json

f = open('Input data/level1b.json')
d = json.load(f)
neighbour=d['neighbourhoods']
ord_quantity=[]
distance=[]
for i in neighbour.keys():
    temp=list(neighbour[i].values())
    ord_quantity.append(temp[0])
    distance.append(temp[1])

res_dist=d['restaurants']['r0']['neighbourhood_distance']

print("Distance to neighbourhood from restaurant r0 :",res_dist)

print("Order_quantity for each area ",ord_quantity)

max_cap=d['vehicles']['v0']['capacity']

print("capacity of scooter :",max_cap)

print("Total quantity :",sum(ord_quantity))

print("minimum number of slots :",round(sum(ord_quantity)/max_cap))

import itertools

def nearest_neighbor(distance_matrix, ord_quantity, max_cap):
    unvisited = set(range(len(distance_matrix)))
    current_node = 0  # Start from node 0
    current_capacity = 0
    current_distance = 0
    slots = []
    current_slot=[]
    while unvisited:
        unvisited.remove(current_node)
        if current_capacity + ord_quantity[current_node] <= max_cap:
            current_capacity += ord_quantity[current_node]
            current_slot.append(current_node)
        else:
            slots.append((current_slot, current_distance))
            current_slot = [current_node]
            current_capacity = ord_quantity[current_node]
            current_distance = 0

        if unvisited:
            next_node = min(unvisited, key=lambda x: distance_matrix[current_node][x])
            current_distance += distance_matrix[current_node][next_node]
            current_node = next_node

    if current_slot:
        slots.append((current_slot, current_distance))

    return slots



slots = nearest_neighbor(distance, ord_quantity, max_cap)
final_lst=[]
for i in slots:
    temp=[]
    temp.append('r0')
    for j in i[0]:
        temp.append('n'+str(j))
    temp.append('r0')
    final_lst.append(temp)
print(final_lst)
final_slots={"v0": {"path1": final_lst[0], "path2": final_lst[1], "path3": final_lst[2],"path4":final_lst[3]}}

with open("level1b_output.json", "w") as outfile:
    json.dump(final_slots, outfile)



