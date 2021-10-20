import numpy as np
from math import sqrt

def order_time(order, drones, warehouses, P, product_weights, drone_capacity):
    # Divy up order into deliveries of acceptable weight
    deliveries = [[0] * P]
    for i in np.argsort(np.array(product_weights)):
        for k in range(order.itemsbytype[i]):
            if sum(deliveries[-1][j] * product_weights[j] for j in range(P)) + product_weights[i] >= drone_capacity:
                deliveries.append([0] * P)
            deliveries[-1][i] += 1

    # Find items in warehouses
    route = [] * len(deliveries)
    assignments = [] * len(deliveries)
    for l, d in enumerate(deliveries):
        route[l] = []
        assignments[l] = {}
        d_ = d.copy()
        while sum(d_) > 0:
            wd = [[0] * P] * len(warehouses)
            for w in warehouses:
                for i in range(P):
                    wd[w, i] = min(w.availability[i], d_[i])
            best_warehouse = sorted(range(len(wd)), key=lambda i: -sum(wd[i]))[0]
            assignments[best_warehouse] = wd[best_warehouse]
            route.append(best_warehouse)
            d_change = [x - y for x, y in zip(d_, wd[best_warehouse])]
            if d_change == d_:
                return -1
            d_ = d_change
    
    # Calculate time of routes
    time = 0
    drone_assignments = [] * len(deliveries)
    for l in range(len(deliveries)):
        # Assign drone
        min_drone = np.inf
        for d in drones:
            dist = sqrt((d.col - warehouses[route[l][0]].col)**2 + (d.row - warehouses[route[l][0]].row)**2)
            if dist < min_drone:
                min_drone = dist
                drone_assignments[l] = d
        
        # Calculate time
        time += min_drone
        pos = (warehouses[route[l][0]].col, warehouses[route[l][0]].row)
        for k in route[l][1:]:
            pos_ = (warehouses[k].col, warehouses[k].row)
            time += sqrt((pos[0] - pos_[0])**2 + (pos[1] - pos_[1])**2)
            pos = pos_
        time += sqrt((pos[0] - pos_[0])**2 + (pos[1] - pos_[1])**2)
