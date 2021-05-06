import numpy as np
from sklearn.cluster import KMeans
import math
import time

nodesfile = open("dataset/cal.cnode","r")
edgesfile = open("dataset/cal.cedge","r")

nodes = []
edges = []

for node in nodesfile:
	nodes.append(node.split())

for edge in edgesfile:
	edges.append(edge.split())

def get_adjacent_nodes(node,edges):
	adj_nodes = []
	for edge in edges:
		if(str(node) == edge[1]):
			adj_nodes.append(edge[2])
		elif(str(node) == edge[2]):
			adj_nodes.append(edge[1])
	return adj_nodes

def get_edge_dist(node1,node2):
	for edge in edges:
		if(str(node1) == edge[1]):
			if(str(node2) == edge[2]):
				return float(edge[3])
		elif(str(node1) == edge[2]):
			if(str(node2) == edge[1]):
				return float(edge[3])	

def get_xy_node(mynode,nodes):
	for node in nodes:
		if(str(mynode) == node[0]):
			return [node[1],node[2]]

def euclidean_distance(node1,node2,nodes):
	xy1 = get_xy_node(node1,nodes)
	xy2 = get_xy_node(node2,nodes)
	return math.sqrt((float(xy1[0])-float(xy2[0]))**2 + (float(xy1[1])-float(xy2[1]))**2)


def astar(startnode,endnode,edges,nodes):
	open_list = [startnode]
	closed_list = []
	parent = {}
	fn = {}
	gn = {}
	hn = {}
	gn[startnode] = 0
	hn[startnode] = euclidean_distance(startnode,endnode,nodes)
	fn[startnode] = gn[startnode] + hn[startnode]

	while(len(open_list)!=0):
		print("Open: ",open_list)
		print("Closed",closed_list)
		min_node = None
		min_fn_value = 9999999
		for node in open_list:
			if(min_fn_value > fn[node]):
				min_node = node
				min_fn_value = fn[node]
		closed_list.append(min_node)
		open_list.remove(min_node)
		adj_nodes2 = get_adjacent_nodes(min_node,edges)
		for adj_node in adj_nodes2:
			if(adj_node in closed_list):
				pass
			elif(adj_node not in open_list):
				open_list.append(adj_node)
				parent[adj_node] = min_node
				gn[adj_node] = gn[min_node] + get_edge_dist(adj_node,min_node)
				hn[adj_node] = euclidean_distance(adj_node,endnode,nodes)
				fn[adj_node] = gn[adj_node] + hn[adj_node]
			elif(adj_node in open_list):
				if(gn[min_node] + get_edge_dist(adj_node,min_node)<gn[adj_node]):
					parent[adj_node] = min_node
					gn[adj_node] = gn[min_node] + get_edge_dist(adj_node,min_node)
					hn[adj_node] = euclidean_distance(adj_node,endnode,nodes)
					fn[adj_node] = gn[adj_node] + hn[adj_node]
		if(endnode in closed_list):
			break
	if(len(open_list)==0):
		print("Failed")
	print("\nDistance value: ",fn[min_node]," degrees in latitude")
	print(fn[min_node]*111," kilometers")
	print("\nRoute: ")
	while(min_node != startnode):
		print(min_node)
		min_node = parent[min_node]
	print(startnode)

start = time.time()
astar("0","277",edges,nodes)
end = time.time()
print("Execution time: ",(end-start))