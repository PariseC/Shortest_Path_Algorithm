import csv
import sys
import matplotlib.pyplot as plt
from queue import PriorityQueue

class Network():
    def __init__(self):
        self.source_node_id=None
        self.sink_node_id=None

        self.node_id_list=[]
        self.node_x_coord={}
        self.node_y_coord={}
        self.node_neighbors={}
        self.number_of_nodes=0
        self.link_list=[]
        self.link_cost={}


def read_data(node_file,link_file,net):
    #read node csv file
    with open(node_file) as f:
        node_reader = csv.reader(f)
        next(node_reader)
        for row in node_reader:
            net.node_id_list.append(int(row[0]))
            net.node_x_coord[int(row[0])]=float(row[1])
            net.node_y_coord[int(row[0])]=float(row[2])
            net.node_neighbors[int(row[0])]=[]
    #read link csv file
    with open(link_file) as f:
        link_reader=csv.reader(f)
        next(link_reader)
        for row in link_reader:
            from_node_id=int(row[1])
            to_node_id=int(row[2])
            cost=float(row[3])
            net.node_neighbors[from_node_id].append(to_node_id)
            net.link_list.append([from_node_id,to_node_id])
            net.link_cost[from_node_id,to_node_id]=cost
    net.number_of_nodes=len(net.node_id_list)

def evaluate_remaining_distance(current,net):
    return abs(net.node_x_coord[current]-net.node_x_coord[net.sink_node_id])\
           +abs(net.node_y_coord[current]-net.node_y_coord[net.sink_node_id])

def show_shortest_path(net,path_node_id_list):
    for from_node_id,to_node_id in net.link_list:
        x_coords=[net.node_x_coord[from_node_id],net.node_x_coord[to_node_id]]
        y_coords=[net.node_y_coord[from_node_id],net.node_y_coord[to_node_id]]
        plt.plot(x_coords,y_coords,color='black',linewidth=0.5)
    path_x_coord=[]
    path_y_coord=[]
    for node_id in path_node_id_list:
        path_x_coord.append(net.node_x_coord[node_id])
        path_y_coord.append(net.node_y_coord[node_id])
    plt.plot(path_x_coord,path_y_coord,color='b')
    plt.xlabel('x_coord')
    plt.ylabel('y_coord')
    plt.show()

def find_shortest_path(net):
    frontier = PriorityQueue()
    frontier.put((net.source_node_id,0))
    came_from = {}
    cost_so_far = {}
    came_from[net.source_node_id] = None
    cost_so_far[net.source_node_id] = 0

    while not frontier.empty():
        current=frontier.get()[0]

        if current == net.sink_node_id:
            break

        for next_node in net.node_neighbors[current]:
            new_cost = cost_so_far[current] + net.link_cost[current, next_node]
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + evaluate_remaining_distance(next_node,net)
                frontier.put((next_node,priority))
                came_from[next_node] = current

    path_node_id_list=[net.sink_node_id]
    pre_node_id=came_from[net.sink_node_id]
    path_cost=0
    while pre_node_id!=net.source_node_id:
        path_node_id_list.insert(0,pre_node_id)
        path_cost+=net.link_cost[path_node_id_list[0],path_node_id_list[1]]
        pre_node_id=came_from[pre_node_id]
    path_node_id_list.insert(0,net.source_node_id)
    path_cost += net.link_cost[path_node_id_list[0], path_node_id_list[1]]
    path='-'.join( [ str(i) for i in path_node_id_list] )

    print("the trave cost from node id=%s to node id=%s is: %s"%(net.source_node_id,net.sink_node_id,path_cost))
    print("the shortest path from node id=%s to node id=%s is: %s"%(net.source_node_id,net.sink_node_id,path))

    show_shortest_path(net,path_node_id_list)

if __name__=='__main__':
    net=Network()
    net.source_node_id=4298
    net.sink_node_id=169
    read_data('./node.csv','./link.csv',net)

    if net.source_node_id not in net.node_id_list:
        print(" %s not found"%net.source_node_id)
        sys.exit(0)
    if net.sink_node_id not in net.node_id_list:
        print(" %s not found"%net.sink_node_id)
        sys.exit(0)

    find_shortest_path(net)