from Algorithm1 import Algo1 
import numpy as np
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

def cal_u(cid,rid,S,s1,t1,utility,sim,cost):
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
	return u1*0.5+u2*0.3+u3*0.2

def cal_u_car(cid,S,utility,sim,cost,quests):
	riders = set([])
	for x in S:
		riders = riders | x['riders']
	sum_u = 0	
	for rid in riders:
		sum_u += cal_u(cid,rid,S,quests[rid][0],quests[rid][3],utility,sim,cost)
	return sum_u

def efficiencyGreedy(cost,cars,quests,utility,S,sim):
	pairSet = []
	a1 = Algo1(cost)
	for qi in range(len(quests)):
		for ci in range(len(cars)):
			tmpS = a1.ScheduleSingleRequest(S[ci],cars[ci],quests[qi],qi);
			if tmpS:
				cost1 = calCost(S[ci],cost);
				cost2 = calCost(tmpS,cost);
				u0 = cal_u_car(ci,S[ci],utility,sim,cost,quests)
				u1 = cal_u_car(ci,tmpS,utility,sim,cost,quests)
				pairSet.append([qi,ci,(u1-u0)*1.0/(cost2-cost1+0.001)])
	
	pairSet = sorted(pairSet,key= lambda x:x[2],reverse=True)
	while pairSet:
		# print pairSet
		qi = pairSet[0][0]
		ci = pairSet[0][1]
		S[ci] = a1.ScheduleSingleRequest(S[ci],cars[ci],quests[qi],qi);
		#print S[ci]
                del pairSet[0]
		# print "qi,ci",qi,ci 
		for i in range(len(pairSet)-1,-1,-1):
			if pairSet[i][0]==qi:
				del pairSet[i]
				continue
			if pairSet[i][1]==ci:
				tmpS = a1.ScheduleSingleRequest(S[ci],cars[ci],quests[pairSet[i][0]],pairSet[i][0])
				if tmpS:
					cost1 = calCost(S[ci],cost)
					cost2 = calCost(tmpS,cost)
					u0 = cal_u_car(ci,S[ci],utility,sim,cost,quests)
					u1 = cal_u_car(ci,tmpS,utility,sim,cost,quests)
					pairSet[i][2] = (u1-u0)*1.0/(cost2-cost1+0.01)
				else:
					del pairSet[i]
		pairSet = sorted(pairSet,key= lambda x:x[2],reverse=True)
	# print S
	return S

# def efficiencyGreedy_old(cost,cars,quests,utility,S):
# 	pairSet = []
# 	a1 = Algo1(cost)
# 	for qi in range(len(quests)):
# 		for ci in range(len(cars)):
# 			tmpS = a1.ScheduleSingleRequest(S[ci],cars[ci],quests[qi],qi);
# 			if tmpS:
# 				cost1 = calCost(S[ci],cost);
# 				cost2 = calCost(tmpS,cost);
# 				pairSet.append([qi,ci,utility[qi][ci]*1.0/(cost2-cost1+0.001)])
	
# 	pairSet = sorted(pairSet,key= lambda x:x[2],reverse=True)
# 	while pairSet:
# 		# print len(pairSet)
# 		# print pairSet
# 		qi = pairSet[0][0]
# 		ci = pairSet[0][1]
# 		S[ci] = a1.ScheduleSingleRequest(S[ci],cars[ci],quests[qi],qi);
# 		del pairSet[0]
# 		# print "qi,ci",qi,ci 
# 		for x in pairSet:
# 			if x[0]==qi:
# 				del x
# 				continue
# 			if x[1]==ci:
# 				tmpS = a1.ScheduleSingleRequest(S[ci],cars[ci],quests[x[0]],x[0])
# 				if tmpS:
# 					cost1 = calCost(S[ci],cost)
# 					cost2 = calCost(tmpS,cost)
# 					x[2] = utility[x[0]][ci]*1.0/(cost2-cost1+0.01)
# 				else:
# 					del x
# 	# print S
# 	return S

# start = clock();
# S = efficiencyGreedy(cost,cars,quests,S)
# end = clock();
# print "time:", end-start
