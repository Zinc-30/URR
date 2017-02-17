import os
import networkx as nx
from math import pow,sqrt
from random import randint
from random import random
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
	noden = len(nodeid)
	for line in open(filename,'r'):
		i = i+1
		tmps = line[:-1].split(' ')
		if tmps[0] == 'a' and tmps[1] in nodeid and tmps[2] in nodeid:
			w = int(tmps[3])//2
			t1 = nodeid.index(tmps[1])
			t2 = nodeid.index(tmps[2])
#			while w>1000:
#				w = w - 1000
#				noden=noden+1
#				t2 = noden
#				G.add_edge(t1, t2, weight=w)
#				t1 = t2
			G.add_edge(t1, nodeid.index(tmps[2]), weight=w)
	return G

def sQuest(filename,area,nodes,times,pt1):
	i = 1
	limit = 3000
	quest = [];
	# for line in open(filename,'r'):

		# tmps = line[:-1].split(',')	
		# if 2<i:
			# bnode = [int(float(tmps[10])*1000000),int(float(tmps[11])*1000000)]
			# enode = [int(float(tmps[12])*1000000),int(float(tmps[13])*1000000)]
			# if inArea(bnode,area) and inArea(enode,area):
			# 	array1 = [int(sqrt(pow(bnode[0]-node[1],2)+pow(bnode[1]-node[2],2))) for node in nodes]
			# 	array2 = [int(sqrt(pow(enode[0]-node[1],2)+pow(enode[1]-node[2],2))) for node in nodes]
			# 	mindist1 = min(array1)
			# 	mindist2 = min(array2)
			# 	if mindist1<limit and mindist2<limit:
			# 		node1 = array1.index(mindist1)
			# 		node2 = array2.index(mindist2)
	for line in range(1000):
		for k in range(times):
			time1 = randint(pt1+1,pt1+300)
			time2 = int(time1+200+2*randint(100,1000))
			quest.append([randint(0,len(nodes)),time1,time2,randint(0,len(nodes))])
	return quest

def sCars(num,limit,room):
	cars = []
	for i in range(num):
		lid = randint(0,limit)
		cars.append([lid,room])
	return cars


# def sCars(nums):
area = [-74000000,40730000,-73900000,40740000] #664,34
# area = [-74000000,40730000,-73900000,40750000]  #1482,49
# area = [-74000000,40730000,-73900000,40760000] 2164,151
# area = [-74100000,40720000,-73800000,40770000] 9531,449
# area = [-74000000,40710000,-73800000,40770000] 8801,1121

# area = [-74000000,40730000,-73800000,40770000] #5636,941
print "select area",area

nodes = sNodes('data/USA-road-d.NY.co',area)
print "slect node num",len(nodes)

#======================================================
qlen = []
for numQ in [1,3,5,8,10]:
	if numQ == 3:
		for pt in [0,5,10,15]:
			quest = sQuest('data/trip_data_2.csv',area,nodes,numQ,pt*60)
			filename = 'data/'+str(numQ)+'.'+str(pt)+'-quests.npy'
			np.save(filename, np.array(quest))
	else:
		quest = sQuest('data/trip_data_2.csv',area,nodes,numQ,300)
		filename = 'data/'+str(numQ)+'.'+str(5)+'-quests.npy'
		np.save(filename, np.array(quest))
print "generate quest"

for numC in [5,8,10,30,50]:
	if numC == 10:
		for roomC in [2,3,4,5]:
			cars = sCars(numC*100,len(nodes),roomC)
			filename = 'data/'+str(numC)+'.'+str(roomC)+'-cars.npy'
			np.save(filename, np.array(cars))
	else:
		roomC = 3
		cars = sCars(numC*100,len(nodes),roomC)
		filename = 'data/'+str(numC)+'.'+str(roomC)+'-cars.npy'
		np.save(filename, np.array(cars))
print "generate cars"

for numC in [5,8,10,30,50]:
	if numC == 10:
		for ql in [1,3,5,8,10]:
			utility = [[random()/2+0.5 for i in range(numC*100)] for j in range(ql*1000)]
			filename = 'data/'+str(ql)+'.'+str(numC)+'-utility.npy'
			np.save(filename, np.array(utility))
	else:
		utility = [[random()/2+0.5 for i in range(numC*100)] for j in range(3000)]
		filename = 'data/'+str(3)+'.'+str(numC)+'-utility.npy'
		np.save(filename, np.array(utility))
print "generate utility"

#=======================================================

G = sRoad('data/USA-road-d.NY.gr',nodes)
print "generate into G.node num",len(G.nodes())
print "generate into G.edges num",len(G.edges())

cost = nx.shortest_path_length(G,weight='weight')
print "calc cost distance between nodes"

nx.write_gml(G,"data/graph.gml")
np.save('data/nodes.npy', np.array(nodes))
np.save('data/cost.npy', np.array(cost))
print "finish save data"
