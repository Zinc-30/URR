import networkx as nx
import numpy as np
import os

def readRoad():
	G = nx.Graph()
	if os.path.exists('data/graph.gml'):
		G = nx.read_gml("data/graph.gml")
		print 'read road data'
	else:
		print 'no road data'
	return G

def readCost():
	if os.path.exists('data/cost.npy'):
		cost = np.load('data/cost.npy').tolist()
		print 'read cost data';
	else:	
		print 'no cost data'
	return cost

def readQuests(numQ,pt):
	filename = 'data/'+str(numQ)+'.'+str(pt)+'-quests.npy'
	if os.path.exists(filename):
		print 'read request data'
		return np.load(filename).tolist()
	else:
		print 'no request data'

def readCars(numC,roomC):
	filename = 'data/'+str(numC)+'.'+str(roomC)+'-cars.npy'
	if os.path.exists(filename):
		print 'read cars data'
		return np.load(filename).tolist()
	else:
		print 'no cars data'

def readUtility(numQ,numC):
	filename = 'data/'+str(numQ)+'.'+str(numC)+'-utility.npy'
	if os.path.exists(filename):
		print 'read utility data'
		return np.load(filename).tolist()
	else:
		print 'no utility data'

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