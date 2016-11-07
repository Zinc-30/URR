import networkx as nx
import numpy as np
import os
import json
def readRoad(filename):
	G = nx.Graph()
	if os.path.exists('graph.gml'):
		G = nx.read_gml("graph.gml")
		print 'give road'
	else:	
		for line in open(filename):
			tmps = line.split(' ');
			if tmps[0] == 'a':
				G.add_edge(tmps[1], tmps[2], weight=int(tmps[3]))
		nx.write_gml(G,"graph.gml")
	return G

def readCost(G):
	if os.path.exists('cost.npy'):
		cost = np.load('cost.npy').tolist()
		print 'give cost';
	else:	
		cost = nx.shortest_path_length(G,weight='weight')
		np.save('cost.npy', np.array(cost))
	return cost

def readInfo(filename,quests,cars,utility):
	for line in open(filename):
			tmps = line[:-1].split(' ');
			if tmps[0] == 'q':
				quests.append([tmps[1],int(tmps[2]),int(tmps[3]),tmps[4]])
			elif tmps[0] == 'c':
				cars.append([tmps[1],int(tmps[2]),()])
			elif tmps[0] == 'u':
				utility.append([int(x) for x in list(tmps[1:])])
	return 0
# def getG():
# 	G = nx.Graph()
# 	G = readRoad('road.txt',G)
# 	return G

# def getCost():
# 	cost = readCost(G)
# 
# quests = [['A',4,10,'H'],['F',7,10,'H'],['E',5,10,'G'],['G',2,7,'E']]
# cars = [['B',2,()],['D',2,()]] 
# quests = [['1',1000,2000,'2'],['1',7,210,'5'],['332',15,400,'24'],['546',22,723,'1']]
# cars = [['1',2,()],['1',2,()]] 
# utility = [[1,2],[3,2],[1,4],[5,1]]