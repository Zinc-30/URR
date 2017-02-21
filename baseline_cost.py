from Algorithm1 import Algo1 
import readData as rd

def costGreedy(cost,cars,quests,utility,S,sim,paras):
	pairSet = []
	a1 = Algo1(cost)
	for qi in range(len(quests)):
		for ci in range(len(cars)):
			tmpS = a1.ScheduleSingleRequest(S[ci],cars[ci],quests[qi],qi);
			if tmpS:
				cost1 = rd.calCost(S[ci],cost);
				cost2 = rd.calCost(tmpS,cost);
				pairSet.append([qi,ci,cost2-cost1])
	
	pairSet = sorted(pairSet,key= lambda x:x[2],reverse=False)
	while pairSet:
		# print pairSet
		# print len(pairSet)
		# print pairSet
		qi = pairSet[0][0]
		ci = pairSet[0][1]
		S[ci] = a1.ScheduleSingleRequest(S[ci],cars[ci],quests[qi],qi);
		del pairSet[0]
		# print "qi,ci",qi,ci 
		for i in range(len(pairSet)-1,-1,-1):
			if pairSet[i][0]==qi:
				del pairSet[i]
				continue
			if pairSet[i][1]==ci:
				tmpS = a1.ScheduleSingleRequest(S[ci],cars[ci],quests[pairSet[i][0]],pairSet[i][0])
				if tmpS:
					cost1 = rd.calCost(S[ci],cost)
					cost2 = rd.calCost(tmpS,cost)
					pairSet[i][2] = cost2-cost1+0.01
				else:
					del pairSet[i]
		pairSet = sorted(pairSet,key= lambda x:x[2],reverse=False)
	# print S
	return S
