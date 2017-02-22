import Algorithm3
import readData as rd

def purnCars(quests,center,cars,areadict,radius,cost):
	carc = []
	carids = []
	maxt = 0
	for q in quests:
		if q[1] >maxt:
			maxt = q[1]
	for cid in range(len(cars)):
		car = cars[cid]
		if center in radius and rd.getCost(car[0],center,cost)<maxt+radius[center]:
			carc.append(car)
			carids.append(cid)
 	return carc,carids

def groupScheduling(cost,cars,quests,utility,S,areadict,radius,sim,paras):
	g={}
	q2id_g = {}
	grest = []
	q2id_rest = []
	for qi in range(len(quests)):
		q = quests[qi]
		if q[0] in areadict and q[3] in areadict and areadict[q[0]] == areadict[q[3]]:
			ax = areadict[q[0]]
			if ax not in g:
				g[ax] = []
				q2id_g[ax] = []
			g[ax].append(q)
			q2id_g[ax].append(qi)
		else:
			grest.append(q)
			q2id_rest.append(qi)
	gnew = sorted(g,key = lambda x:len(g[x]),reverse=1)
	S = Algorithm3.efficiencyGreedy(cost,cars,grest,utility,S,sim,paras,q2id = q2id_rest,quests_all = quests)
	for c in gnew:
		carc, carcid = purnCars(g[c],c,cars,areadict,radius,cost)
		S = Algorithm3.efficiencyGreedy(cost,carc,g[c],utility,S,sim,paras,c2id = carcid,q2id = q2id_g[c],quests_all = quests)
	return S






