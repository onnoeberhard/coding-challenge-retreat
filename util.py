from scoring import Drone, Action, Warehouse, Order, Manager, Score, JudgeSystem

def read_in_file(inputF):
    """Returns drones, warehouses, grid, orders, number of products, weights of products"""
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
            
    return Drones, Warehouses, Grid, Orders, P, productsWeights