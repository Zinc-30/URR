import networkx as nx
#input=
G = nx.Graph()
G.add_weighted_edges_from([('A','B',1),('B','E',2),('E','H',1),('E','F',1),('F','H',2),('F','G',2),('G','H',3),('D','G',1),('A','D',2),('A','C',1),('C','F',5)])	
cost = nx.shortest_path_length(G,weight='weight');

quests = [['A',4,10,'H'],['E',5,10,'G'],['F',7,10,'H'],['G',2,7,'E']]
cars = [['B',2,()],['D',2,()]] 

#output=
S = []
Sbest = []
#event = {'startLocation':,'startTime':,'flexibleTime':,'riders':(),'endLocation':,'deadline':} 

questId = 0;
carId = 0;

costIncreament = 100000;
Sbest=[]
if S == []:
	print 'empty' 
	event = {'startLocation':cars[carId][0],'startTime':0,'flexibleTime':quests[questId][2] - cost[cars[carId][0]][quests[questId][0]],'riders':(),'endLocation':quests[questId][0],'deadline':quests[questId][2]}
	S.append(event)

print S