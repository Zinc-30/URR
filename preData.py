import os
import networkx as nx
from math import pow,sqrt
from random import randint
import numpy as np

def inArea(node,area):
	return area[0]<=node[0]<=area[2] and area[1]<=node[1]<=area[3]

def sNodes(filename,area):
	i = 0
	nodes = []
	for line in open(filename,'r'):
		tmps = line[:-1].split(' ')
		i = i + 1
		if tmps[0] == 'v':
			nid = tmps[1]
			node = [int(tmps[2]),int(tmps[3])]
			if inArea(node,area):
				nodes.append([nid,node[0],node[1]])
	return nodes

def sRoad(filename,nodes):
	G = nx.Graph()
	nodeid = [x[0] for x in nodes]
	i = 0
	for line in open(filename,'r'):
		i = i+1
		tmps = line[:-1].split(' ')
		if tmps[0] == 'a' and tmps[1] in nodeid and tmps[2] in nodeid:
				G.add_edge(nodeid.index(tmps[1]), nodeid.index(tmps[2]), weight=int(tmps[3]))
	return G

def sQuest(filename,area,nodes):
	i = 1
	limit = 3000
	quest = [];
	for line in open(filename,'r'):
		tmps = line[:-1].split(',')	
		if 2<i:
			bnode = [int(float(tmps[10])*1000000),int(float(tmps[11])*1000000)]
			enode = [int(float(tmps[12])*1000000),int(float(tmps[13])*1000000)]
			if inArea(bnode,area) and inArea(enode,area):
				array1 = [int(sqrt(pow(bnode[0]-node[1],2)+pow(bnode[1]-node[2],2))) for node in nodes]
				array2 = [int(sqrt(pow(enode[0]-node[1],2)+pow(enode[1]-node[2],2))) for node in nodes]
				mindist1 = min(array1)
				mindist2 = min(array2)
				if mindist1<limit and mindist2<limit:
					node1 = array1.index(mindist1)
					node2 = array2.index(mindist2)
					time1 = randint(600,1200)
					time2 = int(time1+1.5*int(tmps[8]))
					quest.append([node1,time1,time2,node2])
		i = i+1
		if i>3000:
			break
	# with open(os.getcwd()+'\\data\\quest.txt','a') as f:
	# 	for x in quest:
	# 		f.write('p',x[0],x[1],x[2],x[3])
	return quest

def sCars(num,limit,room):
	cars = []
	for i in range(num):
		lid = randint(0,limit)
		cars.append([lid,room])
	return cars


# def sCars(nums):
# area = [-74000000,40730000,-73900000,40750000] 1482,49
# area = [-74000000,40730000,-73900000,40760000] 2164,151
# area = [-74100000,40720000,-73800000,40770000] 9531,449
# area = [-74000000,40710000,-73800000,40770000] 8801,1121
area = [-74000000,40730000,-73800000,40770000]
print "select area",area

nodes = sNodes('data/USA-road-d.NY.co',area)
print "slect node num",len(nodes)

G = sRoad('data/USA-road-d.NY.gr',nodes)
print "generate into G.node num",len(G.nodes())
print "generate into G.edges num",len(G.edges())

quest = sQuest('data/trip_data_2.csv',area,nodes)
print "quest num",len(quest)

cars = sCars(300,len(nodes),3)
print "cars num",300

cost = nx.shortest_path_length(G,weight='weight')
print "calc cost distance between nodes"

utility = [[1 for i in range(len(quest))] for j in range(len(cars))]
print "generate utility"

np.save('data/cost.npy', np.array(cost))
np.save('data/quests.npy', np.array(quest))
np.save('data/cars.npy', np.array(cars))
np.save('data/nodes.npy', np.array(nodes))
np.save('data/utility.npy', np.array(utility))
nx.write_gml(G,"data/graph.gml")
print "finish save data"


