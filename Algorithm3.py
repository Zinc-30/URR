from Algorithm1 import Algo1
import readData as rd


def efficiencyGreedy(cost, cars, quests, utility, S, sim, paras, c2id=None, q2id=None):
    pairSet = []
    a1 = Algo1(cost)
    for qi in range(len(quests)):
        for ci in range(len(cars)):
            if c2id:
                cid = c2id[ci]
            else:
                cid = ci
            if q2id:
                qid = q2id[qi]
            else:
                qid = qi
            tmpS = a1.ScheduleSingleRequest(
                S[cid], cars[cid], quests[qid], qid)
            if tmpS:
                cost1 = rd.calCost(S[cid], cost)
                cost2 = rd.calCost(tmpS, cost)
                u0 = rd.cal_u_car(cid, S[cid], utility,
                                  sim, cost, quests, paras)
                u1 = rd.cal_u_car(cid, tmpS, utility, sim, cost, quests, paras)
                pairSet.append(
                    [qid, cid, (u1 - u0) * 1.0 / (cost2 - cost1 + 0.001)])
    pairSet = sorted(pairSet, key=lambda x: x[2], reverse=True)
    while pairSet:
        # print pairSet
        qi = pairSet[0][0]
        ci = pairSet[0][1]
        S[ci] = a1.ScheduleSingleRequest(S[ci], cars[ci], quests[qi], qi)
        # print S[ci]
        del pairSet[0]
        # print "qi,ci",qi,ci
        for i in range(len(pairSet) - 1, -1, -1):
            if pairSet[i][0] == qi:
                del pairSet[i]
                continue
            if pairSet[i][1] == ci:
                tmpS = a1.ScheduleSingleRequest(
                    S[ci], cars[ci], quests[pairSet[i][0]], pairSet[i][0])
                if tmpS:
                    cost1 = rd.calCost(S[ci], cost)
                    cost2 = rd.calCost(tmpS, cost)
                    u0 = rd.cal_u_car(
                        ci, S[ci], utility, sim, cost, quests, paras)
                    u1 = rd.cal_u_car(ci, tmpS, utility, sim,
                                      cost, quests, paras)
                    pairSet[i][2] = (u1 - u0) * 1.0 / (cost2 - cost1 + 0.01)
                else:
                    del pairSet[i]
        pairSet = sorted(pairSet, key=lambda x: x[2], reverse=True)
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
