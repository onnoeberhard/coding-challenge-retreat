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
    route = []
    assignments = []
    for l, d in enumerate(deliveries):
        route.append([])
        assignments.append({})
        d_ = d.copy()
        while sum(d_) > 0:
            wd = [[0] * P for _ in range(len(warehouses))]
            for k, w in enumerate(warehouses):
                for i in range(P):
                    wd[k][i] = min(w.availability[i], d_[i])
            best_warehouse = sorted(range(len(wd)), key=lambda i: -sum(wd[i]))[0]
            assignments[l][best_warehouse] = wd[best_warehouse]
            route[l].append(best_warehouse)
            d_change = [x - y for x, y in zip(d_, wd[best_warehouse])]
            if d_change == d_:
                return -1
            d_ = d_change
    
    print("Routes: ", route)

    # Calculate time of routes
    time = 0
    drone_assignments = []
    for l in range(len(deliveries)):
        # Assign drone
        drone_assignments.append(-1)
        min_drone = np.inf
        for d in drones:
            dist = sqrt((d.col - warehouses[route[l][0]].col)**2 + (d.row - warehouses[route[l][0]].row)**2)
            if dist < min_drone:
                min_drone = dist
                drone_assignments[-1] = d
        
        # Calculate time
        time += min_drone
        pos = (warehouses[route[l][0]].col, warehouses[route[l][0]].row)
        for k in route[l][1:]:
            pos_ = (warehouses[k].col, warehouses[k].row)
            time += sqrt((pos[0] - pos_[0])**2 + (pos[1] - pos_[1])**2)
            pos = pos_
        time += sqrt((pos[0] - order.col)**2 + (pos[1] - order.row)**2)

    return time


if __name__ == '__main__':
    from util import read_in_file
    drones, warehouses, grid, orders, P, product_weights, drone_capacity = read_in_file('simple.in')
    # drones, warehouses, grid, orders, P, product_weights, drone_capacity = read_in_file('busy_day.in')
    for o in orders:
        print(order_time(o, drones, warehouses, P, product_weights, drone_capacity))