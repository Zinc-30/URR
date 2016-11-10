import pickle
import os
import Algorithm3
import Algorithm5
from time import clock

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
def groupScheduling(G,k,cost,cars,quests,utility,S):
	g={}
	grest = []
	area = getArea(G,k,cost)
	start = clock()
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
	# print "grest",grest
	# print "gnew",gnew
	S = Algorithm3.efficiencyGreedy(cost,cars,grest,utility,S)
	for qx in gnew:
		S = Algorithm3.efficiencyGreedy(cost,cars,qx,utility,S)
	end = clock()
	print "time of 6:",end - start
	return S






