import networkx as nx
import Algorithm1
G = nx.Graph()
G.add_weighted_edges_from([('A','B',1),('B','E',2),('E','H',1),('E','F',1),('F','H',2),('F','G',2),('G','H',3),('D','G',1),('A','D',2),('A','C',1),('C','F',5)])	
cost = nx.shortest_path_length(G,weight='weight');
quests = [['A',4,10,'H'],['F',7,10,'H'],['E',5,10,'G'],['G',2,7,'E']]
cars = [['B',2,()],['D',2,()]] 
utility = [[1,2],[3,2],[1,4],[5,1]]
S = [[] for i in range(len(cars))]

def findRiders(S):
	Riders = set()
	for x in S:
		Riders = Riders|x['riders']
	return Riders

def moveRider(S,ri):
	for (i,x) in enumerate(S):
		if i>0:
			if x['riders'] - S[i-1]['riders'] == ri:
				S[i-1]['endLocation'] = x['endLocation']
				S[i-1]['deadline'] = x['deadline']
				S[i-1]['riders'] = x['riders']
				del x
				upId = i-1;
				break;
	for (i,x) in enumerate(S):
		if i>0:
			if  S[i-1]['riders'] - x['riders'] == ri:
				S[i-1]['endLocation'] = x['endLocation']
				S[i-1]['deadline'] = x['deadline']
				S[i-1]['riders'] = x['riders']
				del x
				downId = i-1;
				break;
	for i in range(upId,downId):
		S[i]['riders'] = S[i]['riders'] - ri
	eTime = S[upId]['startTime'];
	for i in range(upId,downId):
		S[i+1]['startTime'] = S[i]['startTime']+cost[S[i]['startLocatioon']][S[i]['endLocation']]
	for i in range(downId,upId,-1):
		if i<len(S)-1:
			S[i]['flexibleTime'] = min(S[i]['deadline'] - S[i]['startTime'] - cost[S[i]['startLocation']][S[i]['endLocation']],S[i+1]['flexibleTime'])
		else:
			S[i]['flexibleTime'] = S[i]['deadline'] - S[i]['startTime'] - cost[S[i]['startLocation']][S[i]['endLocation']];
	return S

def bilateralArrangement(cars,S,quests):
	tmpU = [[[carU,rider.index(carU)] for carU in rider] for rider in utility]
	carList = []
	for li in tmpU:
		carList.append(sorted(li, key= lambda x:x[0],reverse=True))
	questSet = set([i for i in range(len(quests))])

	while questSet:
		questId = questSet.pop();
		while carList[questId]:
			carId = carList[questId][0][1];
			carList[questId].remove(carList[questId][0])
			car = cars[carId]
			request = quests[questId]
			if Algorithm1.ScheduleSingleRequest(S[carId],car,request,questId):
				S[carId] = Algorithm1.ScheduleSingleRequest(S[carId],car,request,questId)
			else:
				riderSet = findRiders(S[carId]);
				riList = []
				while riderSet:
					ri = riderSet.pop();
					riList.append((ri,utility[ri][carId]))
					riList = sorted(riList,key = lambda x:x[1])
				for ri in riList:	
					S[carId] = moveRider(S[carId],ri[0]);
					if Algorithm1.ScheduleSingleRequest(S[carId],car,request,questId):
						S[carId] = Algorithm1.ScheduleSingleRequest(S[carId],car,request,questId)
						carList[ri[0]].append([utility[ri[0]][carId],carId]);
						carList[ri[0]] = sorted(carList[ri[0]],key= lambda x:x[0],reverse=True)
						break;
				print "no solution"
	print S

