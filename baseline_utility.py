from Algorithm1 import Algo1 
import readData as rd

def utilityGreedy(cost,cars,quests,utility,S,sim,paras):
	pairSet = []
	a1 = Algo1(cost)
	for qi in range(len(quests)):
		for ci in range(len(cars)):
			tmpS = a1.ScheduleSingleRequest(S[ci],cars[ci],quests[qi],qi);
			if tmpS:
				u0 = rd.cal_u_car(ci,S[ci],utility,sim,cost,quests,paras)
				u1 = rd.cal_u_car(ci,tmpS,utility,sim,cost,quests,paras)
				pairSet.append([qi,ci,(u1-u0)])
	
	pairSet = sorted(pairSet,key= lambda x:x[2],reverse=True)
	while pairSet:
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
					u0 = rd.cal_u_car(ci,S[ci],utility,sim,cost,quests,paras)
					u1 = rd.cal_u_car(ci,tmpS,utility,sim,cost,quests,paras)
					pairSet[i][2] = (u1-u0)
				else:
					del pairSet[i]
		pairSet = sorted(pairSet,key= lambda x:x[2],reverse=True)
	# print S
	return S
