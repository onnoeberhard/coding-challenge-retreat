from scoring import Drone, Action, Warehouse, Order, Manager, Score, JudgeSystem

def step(action_strings, Drones, Warehouses, Grid, Orders):
    """Executes one time steps of the simulation and return updated objects

    Args:
        action_strings (List[str]): List of Command strings, one entry per line, letters sepperated by one space
        Drones (List[Drone]): List of drones in the simulation
        Warehouses (List[Warehouse]): List of warehouses in the simulation
        Grid (List[List[List[object]]]): Current Grid of the simulation
        Orders (List[Order]): List of Orders of the simulation

    Returns:
        Tuple(List[Drone], List[Warehouse], List[List[List[object]]], List[Order]): Update Object Lists: Drones, Warehouses, Grid, Orders 
    """
    for action_string in action_strings:
        action_string = action_string.split(" ")
        if (len(action_string) > 3):
            action = Action(int(action_string[0]), action_string[1], int(action_string[2]), int(action_string[3]), int(action_string[4]))
        else:
            action = Action(int(action_string[0]), action_string[1], int(action_string[2]))
        drone = Drones[int(action_string[0])]
        drone.addAction(action)
        Drones[int(action_string[0])] = drone
        
    DronesNotU = []
    for drone in Drones:
        if(drone.NumOfActions>0):
            if (drone.isBusy() == False):
                if (drone.getNextActionType()=="U"):
                    Grid, Warehouses, Orders = drone.act(Grid,Warehouses,Orders)
                else:
                    DronesNotU.append(drone.id)
    for y in range(len(Drones)):
        if (Drones[y].id in DronesNotU):
            Grid, Warehouses, Orders = Drones[y].act(Grid,Warehouses,Orders)
            
    return Drones, Warehouses, Grid, Orders 

def read_in_file(inputF):
    """Returns drones, warehouses, grid, orders, number of products, weights of products, drone capacity"""
    with open(inputF) as f:
        content = f.readlines()
        nLine = content[0].split(" ")
        NoR = int(nLine[0])
        NoC = int(nLine[1])
        D = int(nLine[2])
        Drones = []
        for x in range(D):
            drone = Drone(x)
            Drones.append(drone)
        DoS = int(nLine[3])
        MloD = int(nLine[4])
        P = int(content[1])
        productsWeights = [int(x) for x in content[2].split(" ")]
        W = int(content[3])
        line = 4
        Warehouses = []
        Grid = [[[] for x in range(NoC)] for y in range(NoR)]
        for x in range(W):
            nLine = content[line].split(" ")
            ware = Warehouse(x, int(nLine[0]), int(nLine[1]))
            rowWare = int(nLine[0])
            colWare = int(nLine[1])
            if (x == 0):
                for y in range(len(Drones)):
                    Drones[y] = Drone(y, int(nLine[0]), int(nLine[1]))
            line = line + 1
            nLine = content[line].split(" ")
            intlist = []
            for st in nLine:
                intlist.append(int(st))
            ware.setAval(intlist)
            Warehouses.append(ware)
            list = Grid[rowWare][colWare]
            list.append(ware)
            Grid[rowWare][colWare] = list
            line = line + 1
        x = 0
        C = int(content[line])
        line = line + 1
        Orders = []
        for x in range(C):
            nLine = content[line].split(" ")
            ord = Order(x, int(nLine[0]), int(nLine[1]))
            rowOrd = int(nLine[0])
            colOrd = int(nLine[1])
            line = line + 1
            Li = int(content[line])
            ord.setLi(Li)
            line = line + 1
            nLine = content[line].split(" ")
            intlist = []
            for st in nLine:
                intlist.append(int(st))
            intemsByType = [0] * P
            for item in intlist:
                intemsByType[item] = intemsByType[item] + 1
            ord.setItemsbytypes(intemsByType)
            Orders.append(ord)
            list = Grid[rowOrd][colOrd]
            list.append(ord)
            Grid[rowOrd][colOrd] = list
            line = line + 1

    for drone in Drones:
            drone.initializePayload(P)
            
    return Drones, Warehouses, Grid, Orders, P, productsWeights, MloD