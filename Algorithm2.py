from Algorithm1 import Algo1
import readData as rd
import copy
import random

def findRiders(s):
	Riders = set()
	for x in s:
		Riders = Riders|x['riders']
	return Riders

def moveRider(Sc,ri,cost):
	upId = 0
	downId = 0
	S = copy.deepcopy(Sc)
	for (i,x) in enumerate(S):
		if i>0:
			if x['riders'] - S[i-1]['riders'] == set([ri]):
				x['startLocation'] = S[i-1]['startLocation']
				x['startTime'] = S[i-1]['startTime']
				del S[i-1]
				upId = i-1;
				break;
	for (i,x) in enumerate(S):
		if i>0:
			if  S[i-1]['riders'] - x['riders'] == set([ri]):
				S[i-1]['endLocation'] = x['endLocation']
				S[i-1]['deadline'] = x['deadline']
				del x
				downId = i;
				break;
	if S[len(S)-1]['riders'] == set([ri]):
		del S[len(S)-1]
		downId = len(S)-1;

	if upId and downId>upId:
		for i in range(upId,downId):
			S[i]['riders'] = S[i]['riders'] - set([ri])
		if len(S)>0:
			for i in range(upId,len(S)-1):
				S[i+1]['startTime'] = S[i]['startTime']+ rd.getCost(S[i]['startLocation'],S[i]['endLocation'],cost)
			for i in range(downId-1,upId,-1):
				tempTime = [x['deadline'] - x['startTime'] - rd.getCost(x['startLocation'],x['endLocation'],cost) for x in S];
				tempTime.reverse()
				fTime = tempTime[0]
				S.reverse()
				for i in range(len(S)):
					fTime = min(fTime,tempTime[i])
					if fTime<0:
						return [];
					S[i]['flexibleTime'] = fTime;
				S.reverse()
	return S

def bilateralArrangement(cost,cars,quests,utility,S,sim,paras,c2id=None, q2id=None,quests_all=None):
	# tmpU = [[[u,ri] for (ri,u) in enumerate(rider)] for rider in utility]
	# carList = []
	# for li in tmpU:
	# 	carList.append(sorted(li, key= lambda x:x[0],reverse=True))
	if not quests_all:
		quests_all = quests
	validmap = [[1 for i in range(len(cars))] for j in range(len(quests))]
	questSet = set(range(len(quests)))
	a1 = Algo1(cost)
	if q2id:
		id2q = dict(zip(q2id, range(len(q2id))))
	while questSet:
		ri = random.sample(questSet, 1)[0]
		questSet.remove(ri)
		max_u = 0
		carid = -1
		max_q = -1
		max_s = []
		for ci in range(len(cars)):
			if validmap[ri][ci]:
				if c2id:
					cid = c2id[ci]
				else:
					cid = ci
				if q2id:
					rid = q2id[ri]
				else:
					rid = ri
				u_now = rd.cal_u_car(cid,S[cid],utility,sim,cost,quests_all,paras)
				tmps1 = a1.ScheduleSingleRequest(S[cid],cars[cid],quests[ri],rid)
				if tmps1:
					u_after = rd.cal_u_car(cid,tmps1,utility,sim,cost,quests_all,paras)
					if u_after-u_now > max_u:
						max_u = u_after-u_now
						carid = ci
						max_s = tmps1
					elif u_after-u_now==max_u and rd.calCost(tmps1,cost)<rd.calCost(S[cid],cost):
						carid = ci
						max_s = tmps1
				else:		
					riders_inS = findRiders(S[cid])
					for qi in riders_inS:
						tmps1 = moveRider(S[cid],qi,cost)
						tmps2 = a1.ScheduleSingleRequest(tmps1,cars[cid],quests[ri],rid)
						if tmps2:
							u_after = rd.cal_u_car(cid,tmps2,utility,sim,cost,quests_all,paras)
							if u_after-u_now > max_u:
								max_u = u_after-u_now
								max_s = tmps2
								carid = ci
								if q2id:
									max_q = id2q[qi]
								else:
									max_q = qi
							elif u_after-u_now==max_u and rd.calCost(tmps2,cost)<rd.calCost(S[cid],cost):
								carid = ci
								max_s = tmps2
								if q2id:
									max_q = id2q[qi]
								else:
									max_q = qi 
		if carid>=0:
			validmap[ri][carid] = 0
			if c2id:
				cid = c2id[carid]
			else:
				cid = carid
			S[cid] = max_s
			if max_q>=0:
				validmap[max_q][carid] = 1
				questSet.add(max_q)	
	return S

# def bilateralArrangement_old(cost,cars,quests,utility,S):
# 	tmpU = [[[u,ri] for (ri,u) in enumerate(rider)] for rider in utility]
# 	carList = []
# 	for li in tmpU:
# 		carList.append(sorted(li, key= lambda x:x[0],reverse=True))
# 	questSet = set(range(len(quests)))
# 	a1 = Algo1(cost)
# 	while questSet:
# 		questId = questSet.pop();
# 		arrange = 0
# 		while not arrange:
# 			if questId < len(carList) and carList[questId]:
# 				carId = carList[questId][0][1]
# 			else:
# 				# print carList[questId],questId
# 				break
# 			del carList[questId][0]
# 			# print "carId",carId
# 			car = cars[carId]
# 			request = quests[questId]
# 			# print "before",S[carId]
# 			tmps1=a1.ScheduleSingleRequest(S[carId],car,request,questId)
# 			if tmps1:
# 				# print "in change"
# 				S[carId] = tmps1
# 				# print S[carId]
# 				arrange = 1;
# 			else:
# 				# print "after",S[carId]
# 				riderSet = findRiders(S[carId]);
# 				# print "riderSet",riderSet
# 				riList = []
# 				while riderSet:
# 					ri = riderSet.pop();
# 					riList.append((ri,utility[ri][carId]))
# 					riList = sorted(riList,key = lambda x:x[1])
# 				for ri in riList:	
# 					if utility[ri[0]][carId]<utility[questId][carId]:
# 						tmpS = copy.deepcopy(S[carId]) 
# 						S[carId] = moveRider(S[carId],ri[0],cost);
# 						# print " last carID",carId
# 						tmps1=a1.ScheduleSingleRequest(S[carId],car,request,questId)
# 						if tmps1:
# 							S[carId] = tmps1
# 							carList[ri[0]].append([utility[ri[0]][carId],carId]);
# 							carList[ri[0]] = sorted(carList[ri[0]],key= lambda x:x[0],reverse=True)
# 							questSet.add(ri[0])
# 							arrange = 1
# 							break
# 						else:
# 							S[carId] = tmpS
# 	return S
