import numpy as np
from sklearn.cluster import AgglomerativeClustering
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

newnodes = open("dataset/newcal.cnode","r")
trimmednodes = []
counter = 0
for node in newnodes:
	trimmednodes.append(node.split())
	counter += 1

X = np.array(trimmednodes)

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

def get_cluster_of_node(clusters,node):
	for cluster in range(len(clusters)):
		if(int(node) in clusters[cluster]):
			return cluster

def get_xy_node(mynode,nodes):
	for node in nodes:
		if(str(mynode) == node[0]):
			return [node[1],node[2]]

def euclidean_distance(node1,node2,nodes):
	xy1 = get_xy_node(node1,nodes)
	xy2 = get_xy_node(node2,nodes)
	return math.sqrt((float(xy1[0])-float(xy2[0]))**2 + (float(xy1[1])-float(xy2[1]))**2)

def get_clusters(k,array):
	# k = 1345
	# km=KMeans(n_clusters=k)
	km = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='ward')
	km=km.fit(array)
	cluster_labels=km.labels_ # get cluster label of all data
	print("cluster labels of points:", cluster_labels)

	clusters = []

	for i in range(k):
		clusters.append(np.where(cluster_labels==i)[0])
		print("indexes of points in cluster ",i,":", np.where(cluster_labels==i)[0])
	return clusters

def dist_bw_clusters(cluster1,cluster2,nodes,clusters):
	min_distance = 9999999
	for node1 in clusters[cluster1]:
		for node2 in clusters[cluster2]:
			dist = euclidean_distance(node1,node2,nodes)
			if(dist < min_distance):
				min_distance = dist
	return min_distance

def astar(startnode,endnode,edges,nodes,clusters):
	
	open_list = [startnode]
	closed_list = []
	parent = {}
	fn = {}
	gn = {}
	hn = {}
	gn[startnode] = 0
	hn[startnode] = dist_bw_clusters(get_cluster_of_node(clusters,startnode),get_cluster_of_node(clusters,endnode),nodes,clusters)
	fn[startnode] = gn[startnode] + hn[startnode]

	# clusters = get_clusters(1345,edges)
	while(len(open_list)!=0):
		# print("Open: ",open_list)
		# print("Closed",closed_list)
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
				hn[adj_node] = dist_bw_clusters(get_cluster_of_node(clusters,adj_node),get_cluster_of_node(clusters,endnode),nodes,clusters)
				fn[adj_node] = gn[adj_node] + hn[adj_node]
			elif(adj_node in open_list):
				if(gn[min_node] + get_edge_dist(adj_node,min_node)<gn[adj_node]):
					parent[adj_node] = min_node
					gn[adj_node] = gn[min_node] + get_edge_dist(adj_node,min_node)
					hn[adj_node] = dist_bw_clusters(get_cluster_of_node(clusters,adj_node),get_cluster_of_node(clusters,endnode),nodes,clusters)
					fn[adj_node] = gn[adj_node] + hn[adj_node]
		if(endnode in closed_list):
			break
	if(len(open_list)==0):
		print("Failed")
	print("Distance value: ",fn[min_node]," degrees in latitude")
	print("Route: ")
	while(min_node != startnode):
		print(min_node)
		min_node = parent[min_node]
	print(startnode)

clusters = get_clusters(1345,X)
# c1 = get_cluster_of_node(clusters,"326")
# c2 = get_cluster_of_node(clusters,"0")
# print(dist_bw_clusters(c1,c2,nodes,clusters))
start = time.time()
astar("0","277",edges,nodes,clusters)
end = time.time()
print("Execution time: ",(end-start))