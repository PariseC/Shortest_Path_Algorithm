# _*_coding:utf-8 _*_
# @Time　　:2020/2/29/21:32
# @Author　 : Dr.Prase
#@ File　　  :generic label correcting algorithm.py
#@Software  :PyCharm
"""导入相关基础包，定义全局变量"""
import pandas as pd
import numpy as np
import copy
g_node_list=[] #网络节点集合
g_node_zone={}#网络节点类别集合
g_link_list=[] #网络弧集合
g_shortest_path=[]#最短路径集合
g_origin=None   #网络源节点
g_number_of_nodes=0#网络节点个数
node_predecessor=[]#前向节点集合
node_label_cost=[]#距离标签集合
Max_label_cost=99999#初始距离标签
"""导入网络数据文件，构建基础网络并初始化相关变量"""
#读取网络节点数据
df_node=pd.read_csv('node.csv')
df_node=df_node.iloc[:,:].values
for i in range(len(df_node)):
    g_node_list.append(df_node[i,0])
    g_node_zone[df_node[i,0]]=df_node[i,-1]
    g_number_of_nodes+=1
    if df_node[i,3]==1:
        g_origin=df_node[i,0]
Distance=np.ones((g_number_of_nodes,g_number_of_nodes))*Max_label_cost #距离矩阵
node_predecessor=[-1]*g_number_of_nodes
node_label_cost=[Max_label_cost]*g_number_of_nodes
node_predecessor[g_origin-1]=0
node_label_cost[g_origin-1] = 0
#读取网络弧数据
df_link=pd.read_csv('road_link.csv')
df_link=df_link.iloc[:,:].values
for i in range(len(df_link)):
    g_link_list.append((df_link[i,1],df_link[i,2]))
    Distance[df_link[i,1]-1,df_link[i,2]-1]=df_link[i,3]
"""最短路径求解：扫描网络弧，依据检查最优性条件更新距离标签"""
while True:
    v=0# 未满足最优性条件的节点个数
    for head,tail in g_link_list:
        if node_label_cost[tail-1]>node_label_cost[head-1]+Distance[head-1,tail-1]:
            node_label_cost[tail-1]=node_label_cost[head-1]+Distance[head-1,tail-1]
            node_predecessor[tail-1]=head
            v=v+1
    if v==0:
        break
"""依据前向节点生成最短路径"""
agent_id=1
o_zone_id=g_node_zone[g_origin]
for destination in g_node_list:
    if g_origin!=destination:
        d_zone_id=g_node_zone[destination]
        if node_label_cost[destination-1]==Max_label_cost:
            path=" "
            g_shortest_path.append([agent_id,o_zone_id,d_zone_id,path,node_label_cost[destination-1]])
        else:
            to_node=copy.copy(destination)
            path="%s"%to_node
            while node_predecessor[to_node-1]!=g_origin:
                path="%s;"%node_predecessor[to_node-1]+path
                g=node_predecessor[to_node-1]
                to_node=g
            path="%s;"%g_origin+path
            g_shortest_path.append([agent_id,o_zone_id,d_zone_id, path, node_label_cost[destination - 1]])
            print('from {} to {} the path is {}，length is {}'
                      .format(g_origin,destination,path,node_label_cost[destination-1]))
        agent_id+=1
"""将求解结果导出到csv文件"""
#将数据转换为DataFrame格式方便导出csv文件
g_shortest_path=np.array(g_shortest_path)
col=['agent_id','o_zone_id','d_zone_id','node_sequence','distance']
file_data = pd.DataFrame(g_shortest_path, index=range(len(g_shortest_path)),columns=col)
file_data.to_csv('agent.csv',index=False)