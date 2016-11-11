import pickle
import os
import Algorithm3
import Algorithm5
from time import clock

def getCost(x,y,cost):
		if x in cost and y in cost[x]:
			return cost[x][y]
		else:
			return 1000000
def getArea(G,k,cost):
	filename = 'data/area-'+str(k)+'.txt'
	if os.path.exists(filename):
		area = pickle.load(open(filename, 'r'))
		print 'get area data'
	else:
		a5 = Algorithm5.Algo5(G,cost)
		area = a5.areaConstruction(k)
		pickle.dump(area, open(filename, 'w'))
		print 'write area data'
	return area

def getDict(k):
	filename = 'data/areadict-'+str(k)+'.npy'
	if os.path.exists(filename):
		print 'read dict data'
		return pickle.load(open(filename, 'r'))
	else:
		print 'no dict data'

def getRadius(k):
	filename = 'data/areaR-'+str(k)+'.npy'
	if os.path.exists(filename):
		print 'read radic data'
		return pickle.load(open(filename, 'r'))
	else:
		print 'no dict data'

def purnCars(quests,center,cars,areadict,radius,cost):
	carc = []
	maxt = 0;
	for q in quests:
                if q[1] >maxt:
                	maxt = q[1]
	for car in cars:
		    if center in radius and getCost(car[0],center,cost)<maxt+radius[center]:
			    carc.append(car)
 	return carc

def groupScheduling(G,k,cost,cars,quests,utility,S):
	g={}
	grest = []
	area = getArea(G,k,cost)
	areadict = getDict(k)
	radius = getRadius(k)
	for q in quests:
		if q[0] in areadict and q[3] in areadict and areadict[q[0]] == areadict[q[3]]:
			ax = areadict[q[0]]
			if ax not in g:
				g[ax] = []
			g[ax].append(q)
		else:
			grest.append(q)
	gnew = [[g[t],t] for t in sorted(g,key = lambda x:len(g[x]),reverse=1)]
	# print "grest",grest
	# print "gnew",gnew
	S = Algorithm3.efficiencyGreedy(cost,cars,grest,utility,S)
	for gx in gnew:
		carc = purnCars(gx[0],gx[1],cars,areadict,radius,cost)
		S = Algorithm3.efficiencyGreedy(cost,cars,gx[0],utility,S)
	return S






