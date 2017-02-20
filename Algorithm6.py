import Algorithm3
import readData as rd

def purnCars(quests,center,cars,areadict,radius,cost):
	carc = []
	maxt = 0;
	for q in quests:
		if q[1] >maxt:
			maxt = q[1]
	for car in cars:
		if center in radius and rd.getCost(car[0],center,cost)<maxt+radius[center]:
			carc.append(car)
 	return carc

def groupScheduling(cost,cars,quests,utility,S,areadict,radius,sim,paras):
	g={}
	grest = []
	for q in quests:
		if q[0] in areadict and q[3] in areadict and areadict[q[0]] == areadict[q[3]]:
			ax = areadict[q[0]]
			if ax not in g:
				g[ax] = []
			g[ax].append(q)
		else:
			grest.append(q)
	gnew = [[g[t],areadict[g[t][0][0]]] for t in sorted(g,key = lambda x:len(g[x]),reverse=1)]
	print "grest",len(grest)
	print "gnew",len(quests)-len(grest)
	S = Algorithm3.efficiencyGreedy(cost,cars,grest,utility,S,sim,paras)
	for gx in gnew:
		# carc = purnCars(gx[0],gx[1],cars,areadict,radius,cost)
		S = Algorithm3.efficiencyGreedy(cost,cars,gx[0],utility,S,sim,paras)
	return S






