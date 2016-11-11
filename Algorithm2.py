from Algorithm1 import Algo1
import copy

def findRiders(S):
	Riders = set()
	for x in S:
		Riders = Riders|x['riders']
	return Riders

def moveRider(S,ri):
	print "rider",ri
	print "S",S
	for (i,x) in enumerate(S):
		if i>0:
			if x['riders'] - S[i-1]['riders'] == set([ri]):
				x['startLocation'] = S[i-1]['startLocation']
				del S[i-1]
				upId = i-1;
				break;
	for (i,x) in enumerate(S):
		if i>0:
			if  S[i-1]['riders'] - x['riders'] == set([ri]):
				S[i-1]['endLocation'] = x['endLocation']
				S[i-1]['deadline'] = x['deadline']
				del x
				downId = i-1;
				break;
	if S[len(S)-1]['riders'] == set([ri]):
		del S[len(S)-1]
		downId = len(S);
	for i in range(upId,downId):
		S[i]['riders'] = S[i]['riders'] - set([ri])
	if len(S)>0:
		eTime = S[upId]['startTime'];
		for i in range(upId,downId):
			S[i+1]['startTime'] = S[i]['startTime']+ getCost(S[i]['startLocatioon'],S[i]['endLocation'])
		for i in range(downId,upId,-1):
			if i<len(S)-1:
				S[i]['flexibleTime'] = min(S[i]['deadline'] - S[i]['startTime'] - getCost(S[i]['startLocation'],S[i]['endLocation']),S[i+1]['flexibleTime'])
			else:
				S[i]['flexibleTime'] = S[i]['deadline'] - S[i]['startTime'] - getCost(S[i]['startLocation'],S[i]['endLocation']);
	
	return S

def bilateralArrangement(cost,cars,quests,utility,S):
	tmpU = [[[carU,rider.index(carU)] for carU in rider] for rider in utility]
	carList = []
	for li in tmpU:
		carList.append(sorted(li, key= lambda x:x[0],reverse=True))
	questSet = set(range(len(quests)))
	a1 = Algo1(cost)
	while questSet:
		questId = questSet.pop();
		# print "questId",questId
		arrange = 0;
		while not arrange:
			if questId in carList and carList[questId]:
				carId = carList[questId][0][1]
			else:
				# print carList[questId],questId
				break
			carList[questId].remove(carList[questId][0])
			# print "carId",carId
			car = cars[carId]
			request = quests[questId]
			# print "before",S[carId]
			if a1.ScheduleSingleRequest(S[carId],car,request,questId):
				# print "in change"
				S[carId] = a1.ScheduleSingleRequest(S[carId],car,request,questId)
				# print S[carId]
				arrange = 1;
			else:
				# print "after",S[carId]
				riderSet = findRiders(S[carId]);
				# print "riderSet",riderSet
				riList = []
				while riderSet:
					ri = riderSet.pop();
					riList.append((ri,utility[ri][carId]))
					riList = sorted(riList,key = lambda x:x[1])
				for ri in riList:	
					if utility[ri[0]][carId]<utility[questId][carId]:
						tmpS = copy.deepcopy(S[carId]) 
						S[carId] = moveRider(S[carId],ri[0]);
						# print " last carID",carId
						if a1.ScheduleSingleRequest(S[carId],car,request,questId):
							S[carId] = a1.ScheduleSingleRequest(S[carId],car,request,questId)
							carList[ri[0]].append([utility[ri[0]][carId],carId]);
							carList[ri[0]] = sorted(carList[ri[0]],key= lambda x:x[0],reverse=True)
							questSet.add(ri[0])
							arrange = 1
							break
						else:
							S[carId] = tmpS
	return S

