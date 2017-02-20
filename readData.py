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

def getCost(x,y,cost):
	if x in cost and y in cost[x]:
		return cost[x][y]
	else:
		return 1000000

def calCost(S,cost):
	costTime = 0;
	for x in S:
		costTime = costTime + getCost(x['startLocation'],x['endLocation'],cost)
	return costTime

def cal_u(cid,rid,S,s1,t1,utility,sim,cost,paras):
	u1 = utility[rid][cid]
	cost_all = calCost(S,cost)
	u2 = 0
	cost_sum = 0
	for x in S:
		if rid in x['riders']:
			cost_x = getCost(x['startLocation'],x['endLocation'],cost)
			rate = cost_x/cost_all
			for r in x['riders']:
				if r!=rid:
					u2 += rate/(len(x['riders'])-1)*sim[r][rid]
			cost_sum += cost_x
	u3 = 2/(1+np.exp(cost_sum/getCost(s1,t1,cost)))
	return u1*paras[0]+u2*paras[1]+u3*paras[2]

def cal_u_car(cid,S,utility,sim,cost,quests,paras):
	riders = set([])
	for x in S:
		riders = riders | x['riders']
	sum_u = 0	
	for rid in riders:
		sum_u += cal_u(cid,rid,S,quests[rid][0],quests[rid][3],utility,sim,cost,paras)
	return sum_u

def cal_u_all(S,utility,sim,cost,quests,paras):
	ans = 0
	for i in range(len(S)):
		ans += cal_u_car(i,S[i],utility,sim,cost,quests,paras)
	return ans

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