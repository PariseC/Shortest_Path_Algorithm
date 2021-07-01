# -*- coding: utf-8 -*-
# @Time    : 2021/6/28 22:01
# @Author  : CZY
# @File    : deque label correcting algorithm.py
# @Software: PyCharm
# obj : 实现label correcting算法求解最短路问题
import csv
import sys
import matplotlib.pyplot as plt
from collections import deque

# define network data struct
class Network():
    def __init__(self):
        self.node_neighbors={}
        self.node_x_coord={}
        self.node_y_coord={}
        self.node_id_list=[]
        self.number_of_nodes=0
        self.link_cost={}
        self.link_list=[]

        self.source_node_id=0
        self.sink_node_id=1

# read network csv files
def read_network_file(node_file,link_file,network):
    # read node csv file
    with open(node_file) as node_f:
        node_reader=csv.reader(node_f)
        next(node_reader)
        for row in node_reader:
            network.node_id_list.append(int(row[0]))
            network.node_x_coord[int(row[0])] = float(row[1])
            network.node_y_coord[int(row[0])] = float(row[2])
            network.node_neighbors[int(row[0])] = []
    # read link csv file
    with open(link_file) as f:
        link_reader = csv.reader(f)
        next(link_reader)
        for row in link_reader:
            from_node_id = int(row[1])
            to_node_id = int(row[2])
            cost = float(row[3])
            network.node_neighbors[from_node_id].append(to_node_id)
            network.link_list.append([from_node_id, to_node_id])
            network.link_cost[from_node_id, to_node_id] = cost
    network.number_of_nodes = len(network.node_id_list)
    return network

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

# save the shortest path information to csv file
def save_to_file(network,path_node_id_list,path_cost,node_predecessor=None,node_label_cost=None):
    outfile = open('shortest_path.csv', 'w', newline='', errors='ignore')
    write = csv.writer(outfile)

    write.writerow(['source_node_id', 'sink_node_id', 'total cost', 'path node id list'])
    path = '-'.join([str(i) for i in path_node_id_list])
    line = [network.source_node_id, network.sink_node_id,path_cost,path]
    write.writerow(line)
    # whether save the shortest path information from  the source node to other nodes
    if node_predecessor and node_label_cost:
        try:
            for node_id in network.node_id_list:
                if node_id!=network.source_node_id and node_id!=network.sink_node_id:
                    path_node_id_list = [node_id]
                    pre_node_id = node_predecessor[node_id]
                    path_cost = 0
                    if node_label_cost[node_id]<float('inf'):
                        while pre_node_id != network.source_node_id:
                            path_node_id_list.insert(0, pre_node_id)
                            path_cost += network.link_cost[path_node_id_list[0], path_node_id_list[1]]
                            pre_node_id = node_predecessor[pre_node_id]
                        path_node_id_list.insert(0, network.source_node_id)
                        path_cost += network.link_cost[path_node_id_list[0], path_node_id_list[1]]
                        path = '-'.join([str(i) for i in path_node_id_list])
                        line = [network.source_node_id, node_id, path_cost, path]
                        write.writerow(line)
                    else:
                        line = [network.source_node_id, node_id, 'inf', 'nan']
                        write.writerow(line)
        except Exception as e:
            pass
    outfile.close()

# find the shortest path from source node to sink node using deque label correcting algorithm
def find_shortest_path(network):
    node_predecessor = {}
    node_predecessor[network.source_node_id]=None
    node_label_cost = { node_id:float('inf') for node_id in network.node_id_list}
    node_label_cost[network.source_node_id] = 0
    SEList = deque()
    SEList_all = []
    SEList.append(network.source_node_id)
    SEList_all.append(network.source_node_id)
    while len(SEList)>0:
        current_node_id=SEList[0]
        SEList.popleft()
        current_node_label_cost = node_label_cost[current_node_id]
        for to_node_id in network.node_neighbors[current_node_id]:
            new_label=current_node_label_cost+network.link_cost[current_node_id,to_node_id]
            if new_label<node_label_cost[to_node_id]:
                node_label_cost[to_node_id]=new_label
                node_predecessor[to_node_id]=current_node_id
                if to_node_id in SEList_all:
                    SEList.insert(0,to_node_id)
                else:
                    SEList.append(to_node_id)
                SEList_all.append(to_node_id)

    path_node_id_list = [network.sink_node_id]
    pre_node_id = node_predecessor[network.sink_node_id]
    path_cost = 0
    if node_label_cost[network.sink_node_id]<float('inf'):
        while pre_node_id != network.source_node_id:
            path_node_id_list.insert(0, pre_node_id)
            path_cost += network.link_cost[path_node_id_list[0], path_node_id_list[1]]
            pre_node_id = node_predecessor[pre_node_id]
        path_node_id_list.insert(0, network.source_node_id)
        path_cost += network.link_cost[path_node_id_list[0], path_node_id_list[1]]
        path = '-'.join([str(i) for i in path_node_id_list])
        print("the trave cost from node id=%s to node id=%s is: %s" % (network.source_node_id, network.sink_node_id, path_cost))
        print("the shortest path from node id=%s to node id=%s is: %s" % (network.source_node_id, network.sink_node_id, path))

        show_shortest_path(network, path_node_id_list)
        save_to_file(network, path_node_id_list, path_cost,node_predecessor,node_label_cost)
    else:
        print("there is no feasible path from node id=%s to node id=%s"%(network.source_node_id,network.sink_node_id))

if __name__=='__main__':
    # init network data struct
    network=Network()
    # setting source node  id and sink node id
    network.source_node_id=4177
    network.sink_node_id=3881
    # read network files
    read_network_file('./node.csv','./link.csv',network)
    # check whether the source node id and sink node id is in the network
    if network.source_node_id not in network.node_id_list:
        print(" %s not found"%network.source_node_id)
        sys.exit(0)
    if network.sink_node_id not in network.node_id_list:
        print(" %s not found"%network.sink_node_id)
        sys.exit(0)
    # find the shortest path
    find_shortest_path(network)



