import networkx as nx
import SetInfo
import pickle
import os
import Algorithm3
import Algorithm5

G = SetInfo.readRoad('road.txt')
cost = SetInfo.readCost(G)
quests = []
cars = []
utility = []
SetInfo.readInfo('info.txt',quests,cars,utility) 
print "finish loading"
S = [[] for i in range(len(cars))]

def getArea(G,k):
	if os.path.exists('area.txt'):
		area = pickle.load(open("area.txt", "r"))
		print 'give area'
	else:
		a5 = Algorithm5.Algo5(G,cost)
		area = a5.areaConstruction(k)
		pickle.dump(area, open("area.txt", "w"))
		print 'write area'
	return area

def groupScheduling(G,S,cars,quests):
	g={}
	grest = []
	area = getArea(G,3)
	for q in quests:
		for ax in area:
			flag = 1
			if q[0] in area[ax] and q[3] in area[ax]:
				if ax not in g:
					g[ax] = []
				g[ax].append(q)
				flag = 0
				break
		if flag:
			grest.append(q)
	gnew = [g[t] for t in sorted(g,key = lambda x:len(g[x]),reverse=1)]
	print "grest",grest
	print "gnew",gnew
	S = Algorithm3.efficiencyGreedy(cars,S,grest)
	for qx in gnew:
		S = Algorithm3.efficiencyGreedy(cars,S,qx)
	return S

S = groupScheduling(G,S,cars,quests)
print S




