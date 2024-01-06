import json
import itertools

f = open('Input data/level1a.json')
data = json.load(f)
neighbour=data['neighbourhoods']
#let us define two lists to hold order quantity and distances
ord_quantity=[]
dist=[]
for i in neighbour.keys():
    temp=list(neighbour[i].values())
    ord_quantity.append(temp[0])
    dist.append(temp[1])

res_dist=data['restaurants']['r0']['neighbourhood_distance']
max_cap=data['vehicles']['v0']['capacity']

def optimized(slots,dist):
    optimized_slots = []

    for slot, _ in slots:
        possible_orders = itertools.permutations(slot)
        min_dist = float('inf')
        best_order = []

        for order in possible_orders:
            dists = sum(dist[order[i]][order[i+1]] for i in range(len(order) - 1))
            if dists < min_dist:
                min_distance = dists
                best_order = order

        optimized_slots.append((best_order, min_dist))

    return optimized_slots

def knapsack_tps(dist, res_dist, ord_quantities, max_capacity):
    node_order = sorted(range(len(res_dist)), key=lambda x: res_dist[x])
    slots = []
    current_slot = []
    current_capacity = 0
    current_dist = 0

    for node in node_order:
        if current_capacity + ord_quantities[node] <= max_capacity:
            current_slot.append(node)
            current_capacity += ord_quantities[node]

            if len(current_slot) > 1:
                current_dist += dist[current_slot[-2]][current_slot[-1]]
        else:
            slots.append((current_slot, current_dist))
            current_slot = [node]
            current_capacity = ord_quantities[node]
            current_dist = 0

    if current_slot:
        slots.append((current_slot, current_dist))

    return optimized(slots,dist)
    
val=knapsack_tps(dist, res_dist, ord_quantity,max_cap)

#output file coding 
final_lst=[]
for i in val:
    temp=[]
    temp.append('r0')
    for j in i[0]:
        temp.append('n'+str(j))
    temp.append('r0')
    final_lst.append(temp)

final_slots={"v0": {"path1": final_lst[0], "path2": final_lst[1], "path3": final_lst[2],"path4":final_lst[3]}}
print(final_slots)

with open("level1a_output.json", "w") as outfile:
    json.dump(final_slots, outfile)


