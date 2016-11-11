from Algorithm1 import Algo1 

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

def efficiencyGreedy(cost,cars,quests,utility,S):
	pairSet = []
	a1 = Algo1(cost)
	for qi in range(len(quests)):
		for ci in range(len(cars)):
			if a1.ScheduleSingleRequest(S[ci],cars[ci],quests[qi],qi):
				cost1 = calCost(S[ci],cost);
				tmpS = a1.ScheduleSingleRequest(S[ci],cars[ci],quests[qi],qi);
				cost2 = calCost(tmpS,cost);
				pairSet.append([qi,ci,utility[qi][ci]*1.0/(cost2-cost1+0.01)])
	
	pairSet = sorted(pairSet,key= lambda x:x[2],reverse=True)
	while pairSet:
#		print len(pairSet)
		# print pairSet
		qi = pairSet[0][0]
		ci = pairSet[0][1]
		S[ci] = a1.ScheduleSingleRequest(S[ci],cars[ci],quests[qi],qi);
		del pairSet[0]
		# print "qi,ci",qi,ci 
		for x in pairSet:
			if x[0]==qi:
				del x
				continue
			if x[1]==ci:
				if a1.ScheduleSingleRequest(S[ci],cars[ci],quests[x[0]],x[0]):
					cost1 = calCost(S[ci],cost);
					tmpS = a1.ScheduleSingleRequest(S[ci],cars[ci],quests[x[0]],x[0]);
					cost2 = calCost(tmpS,cost);
					# print "costTime",x[0],ci,cost2,cost1
					x[2] = utility[x[0]][ci]*1.0/(cost2-cost1+0.01)
				else:
                                    del x
	# print S
	return S

# start = clock();
# S = efficiencyGreedy(cost,cars,quests,S)
# end = clock();
# print "time:", end-start
