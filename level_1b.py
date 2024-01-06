import json
import itertools

f = open('Input data/level2a.json')
d = json.load(f)

neighbour=d['neighbourhoods']
#let us define two lists to hold order quantity and distances
ord_quantity=[]
distance=[]
for i in neighbour.keys():
    temp=list(neighbour[i].values())
    ord_quantity.append(temp[0])
    distance.append(temp[1])

res_dist=d['restaurants']['r0']['neighbourhood_distance']
max_cap=d['vehicles']['v0']['capacity']

def knapsack(distance, res_dist, ord_quantities, max_cap):
    node_order = sorted(range(len(res_dist)), key=lambda x: res_dist[x])
    slots = []
    current_slot = []
    current_capacity = 0
    current_distance = 0

    for node in node_order:
        if current_capacity + ord_quantities[node] <= max_cap:
            current_slot.append(node)
            current_capacity += ord_quantities[node]

            if len(current_slot) > 1:
                current_distance += distance[current_slot[-2]][current_slot[-1]]
        else:
            slots.append((current_slot, current_distance))
            current_slot = [node]
            current_capacity = ord_quantities[node]
            current_distance = 0

    if current_slot:
        slots.append((current_slot, current_distance))

    optimized_slots = []

    for slot, _ in slots:
        possible_orders = itertools.permutations(slot)
        min_distance = float('inf')
        best_order = []

        for order in possible_orders:
            dist = sum(distance[order[i]][order[i+1]] for i in range(len(order) - 1))
            if dist < min_distance:
                min_distance = dist
                best_order = order

        optimized_slots.append((best_order, min_distance))

    return optimized_slots
os=knapsack(distance, res_dist, ord_quantity,max_cap)

#output file coding 
final_lst=[]
for i in os:
    temp=[]
    temp.append('r0')
    for j in i[0]:
        temp.append('n'+str(j))
    temp.append('r0')
    final_lst.append(temp)
#print(final_lst)
final_slots={"v0": {"path1": final_lst[0], "path2": final_lst[1], "path3": final_lst[2],"path4":final_lst[3],
                    "path5": final_lst[4], "path6": final_lst[5], "path7": final_lst[6],"path8":final_lst[7],
                    "path8": final_lst[9]}}
print(final_slots)

with open("level1b_output.json", "w") as outfile:
    json.dump(final_slots, outfile)


