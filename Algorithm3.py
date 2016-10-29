import Algorithm1
import SetInfo
print "finish import"
G = SetInfo.G
cost = SetInfo.cost
quests = SetInfo.quests
cars = SetInfo.car
utility = SetInfo.utility
print "finish loading"
# G = nx.Graph()
# G.add_weighted_edges_from([('A','B',1),('B','E',2),('E','H',1),('E','F',1),('F','H',2),('F','G',2),('G','H',3),('D','G',1),('A','D',2),('A','C',1),('C','F',5)])	
# cost = nx.shortest_path_length(G,weight='weight');
# quests = [['A',4,10,'H'],['F',7,10,'H'],['E',5,10,'G'],['G',2,7,'E']]
# cars = [['B',2,()],['D',2,()]] 
# utility = [[1,2],[3,2],[1,4],[5,1]]
S = [[] for i in range(len(cars))]

def calCost(S):
	costTime = 0;
	for x in S:
		costTime = costTime + cost[x['startLocation']][x['endLocation']]
	return costTime

def efficiencyGreedy(cars,S,quests):
	pairSet = [];
	for qi in range(len(quests)):
		for ci in range(len(cars)):
			if Algorithm1.ScheduleSingleRequest(S[ci],cars[ci],quests[qi],qi):
				cost1 = calCost(S[ci]);
				tmpS = Algorithm1.ScheduleSingleRequest(S[ci],cars[ci],quests[qi],qi);
				cost2 = calCost(tmpS);
				pairSet.append([qi,ci,utility[qi][ci]*1.0/(cost2-cost1+0.01)])
	while pairSet:
		pairSet = sorted(pairSet,key= lambda x:x[2],reverse=True);
		# print pairSet
		qi = pairSet[0][0]
		ci = pairSet[0][1]
		S[ci] = Algorithm1.ScheduleSingleRequest(S[ci],cars[ci],quests[qi],qi);
		del pairSet[0]
		# print "qi,ci",qi,ci 

		for x in pairSet:
			if x[0]==qi:
				pairSet.remove(x)
				continue
			if x[1]==ci:
				if Algorithm1.ScheduleSingleRequest(S[ci],cars[ci],quests[x[0]],x[0]):
					cost1 = calCost(S[ci]);
					tmpS = Algorithm1.ScheduleSingleRequest(S[ci],cars[ci],quests[x[0]],x[0]);
					cost2 = calCost(tmpS);
					# print "costTime",x[0],ci,cost2,cost1
					x[2] = utility[x[0]][ci]*1.0/(cost2-cost1+0.01)
				else:
					pairSet.remove(x)
	print S
	return S




S = efficiencyGreedy(cars,S,quests)
