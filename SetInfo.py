import networkx as nx
import numpy as np
import os
import json
def readRoad(filename):
	G = nx.Graph()
	if os.path.exists('data/graph.gml'):
		G = nx.read_gml("data/graph.gml")
		print 'give road'
	else:	
		for line in open(filename):
			tmps = line.split(' ');
			if tmps[0] == 'a':
				G.add_edge(tmps[1], tmps[2], weight=int(tmps[3]))
		nx.write_gml(G,"data/graph.gml")
	return G

def readCost(G):
	if os.path.exists('data/cost.npy'):
		cost = np.load('data/cost.npy').tolist()
		print len(cost)
		print 'give cost';
	else:	
		cost = nx.shortest_path_length(G,weight='weight')
		np.save('data/cost.npy', np.array(cost))
	return cost

def readQuests():
	if os.path.exists('data/quests.npy'):
		return np.load('data/quests.npy').tolist()
def readCars():
	if os.path.exists('data/cars.npy'):
		return np.load('data/cars.npy').tolist()
def readUtility():
	if os.path.exists('data/utility.npy'):
		return np.load('data/utility.npy').tolist()

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