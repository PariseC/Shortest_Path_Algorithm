# _*_coding:utf-8 _*_
# @Time　　:2020/3/12/20:14
# @Author　 : Dr.Prase
#@ File　　  :Floyd-Warshall Algorithm.py
#@Software  :PyCharm
"""导入相关基础包，定义全局变量"""
import pandas as pd
import numpy as np
g_node_list=[] #网络节点集合
g_node_zone={}#网络节点类别集合
g_link_list=[] #网络弧集合
g_shortest_path=[]#最短路径集合
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
    g_node_zone[df_node[i, 0]] = df_node[i, -1]
    g_number_of_nodes+=1
node_label_cost=np.ones((g_number_of_nodes,g_number_of_nodes))*Max_label_cost
node_predecessor=np.zeros((g_number_of_nodes,g_number_of_nodes))
for i in range(g_number_of_nodes):
    for j in range(g_number_of_nodes):
        if i==j:
            node_label_cost[i,j]=0
#读取网络弧数据
df_link=pd.read_csv('road_link.csv')
df_link=df_link.iloc[:,:].values
for i in range(len(df_link)):
    g_link_list.append((df_link[i,1],df_link[i,2]))
    node_label_cost[df_link[i,1]-1,df_link[i,2]-1]=df_link[i,3]
    node_predecessor[df_link[i,1]-1,df_link[i,2]-1]=df_link[i,1]
"""最短路径求解：扫描网络弧，依据检查最优性条件更新距离标签"""
for k in g_node_list:
    for arc_head in g_node_list:
        for arc_tail in g_node_list:
            if node_label_cost[arc_head-1,arc_tail-1]>node_label_cost[arc_head-1,k-1]+node_label_cost[k-1,arc_tail-1]:
                    node_label_cost[arc_head-1,arc_tail-1]=node_label_cost[arc_head-1,k-1]+node_label_cost[k-1,arc_tail-1]
                    node_predecessor[arc_head-1,arc_tail-1]=node_predecessor[k-1,arc_tail-1]
"""依据前向节点生成最短路径"""
agent_id=1
for from_node in g_node_list:
    o_zone_id=g_node_zone[from_node]
    for to_node in g_node_list:
        if from_node!=to_node:
            d_zone_id=g_node_zone[to_node]
            if node_label_cost[from_node-1,to_node-1]==Max_label_cost:
                path = " "
            else:
                path = "%s" % to_node
                prior_point=int(node_predecessor[from_node-1,to_node-1])
                while prior_point!=from_node:
                    path = "%s;" %prior_point+path
                    prior_point=int(node_predecessor[from_node-1,prior_point-1])
                path = "%s;" %from_node + path
            g_shortest_path.append([agent_id,o_zone_id,d_zone_id,path,node_label_cost[from_node-1,to_node-1]])
            agent_id+=1
"""将求解结果导出到csv文件"""
#将数据转换为DataFrame格式方便导出csv文件
g_shortest_path=np.array(g_shortest_path)
col=['agent_id','o_zone_id','d_zone_id','node_sequence','distance']
file_data = pd.DataFrame(g_shortest_path, index=range(len(g_shortest_path)),columns=col)
file_data.to_csv('agent.csv',index=False)