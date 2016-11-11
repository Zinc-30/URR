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
		return np.load(filename).tolist()
	else:
		print 'no dict data'

def getRadius(k):
	filename = 'data/areaR-'+str(k)+'.npy'
	if os.path.exists(filename):
		print 'read radic data'
		return np.load(filename).tolist()
	else:
		print 'no dict data'

def purnCars(quests,cars,areadict,radius):
	carc = []
	for q in quests:
		center = areadict[q[0]]
		for car in cars:
			if getCost(car[0],center,cost)<q[1]+radius[center]:
				carc.append(car)
	return carc

def groupScheduling(G,k,cost,cars,quests,utility,S):
	g={}
	grest = []
	area = getArea(G,k,cost)
	areadict = getAdic(k)
	radius = getRadius(k)
	start = clock()
	for q in quests:
		if areadict[q[0]] == areadict[q[3]]:
			ax = areadict[q[0]]
			if ax not in g:
				g[ax] = []
			g[ax].append(q)
		else:
			grest.append(q)
	gnew = [g[t] for t in sorted(g,key = lambda x:len(g[x]),reverse=1)]
	# print "grest",grest
	# print "gnew",gnew
	carc = purnCars(grest,cars,areadict,radius)
	S = Algorithm3.efficiencyGreedy(cost,carc,grest,utility,S)
	for gx in gnew:
		carc = purnCars(gx,cars,areadict,radius)
		S = Algorithm3.efficiencyGreedy(cost,cars,gx,utility,S)
	end = clock()
	print "time of 6:",end - start
	return S






