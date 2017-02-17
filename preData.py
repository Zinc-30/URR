import networkx as nx
import numpy as np
from random import randint
from sklearn.neighbors import KDTree
import pandas as pd

def sNodes(filename):
	i = 0
	nodes = []
	for line in open(filename,'r'):
		tmps = line[:-1].split(' ')
		i = i + 1
		if tmps[0] == 'v':
			node = [int(tmps[2]),int(tmps[3])]
			nodes.append([node[0],node[1]])
	return nodes

def get_nodes_trip(filename,nodes):
	limit = 50
	# calc ==========================
	kdtree = KDTree(nodes)
	df = pd.read_csv(filename,na_values='',dtype={'vendor_id':object,'rate_code':object,'pickup_longitude':float,'pickup_latitude':float,'dropoff_longitude':float,'dropoff_latitude':float})\
		[['pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude','trip_time_in_secs','trip_distance']].dropna()
	pickup_df = df[['pickup_longitude','pickup_latitude']]*1000000
	pickup_df = pickup_df.astype(int)
	dropoff_df = df[['dropoff_longitude','dropoff_latitude']]*1000000
	dropoff_df = dropoff_df.astype(int)
	pickup_dist,pickup_ind = kdtree.query(pickup_df,k=1)
	dropoff_dist,dropoff_ind = kdtree.query(dropoff_df,k=1)
	select_flag = np.logical_and(pickup_dist<limit,dropoff_dist<limit)
	select_df = pd.DataFrame()
	select_df['pickup_nodes'] = pickup_ind[select_flag]
	select_df['dropoff_nodes'] = dropoff_ind[select_flag]
	select_df['cost'] = np.array(df['trip_time_in_secs'])[select_flag.T[0]]
	print select_df.info()	
	select_df = select_df[select_df['pickup_nodes']!=select_df['dropoff_nodes']]
	select_df.to_csv('data/'+str(limit)+'_select_nodes.csv')
	print select_df.info()
	# read ==============================
	select_df = pd.read_csv('data/'+str(limit)+'_select_nodes.csv')
	print select_df.info()
	return set(select_df['pickup_nodes']) | set(select_df['dropoff_nodes'])



def sRoad(filename,nodes):
	G = nx.Graph()
	# calc =======================
	for line in open(filename,'r'):
		tmps = line[:-1].split(' ')
		if tmps[0] == 'a':
			G.add_edge(int(tmps[1]), int(tmps[2]), weight = int(tmps[3]))
	print "generate into G.node num",len(G.nodes())
	print "generate into G.edges num",len(G.edges())
	nodelist = list(nodes)
	cost = dict()
	print "calc cost distance between nodes"
	G_new = nx.Graph()
	for s in nodelist:
		if s not in cost:
			cost[s] = {}
			for t in nodelist:
				if t in cost and s in cost[t]:
					cost[s][t] = cost[t][s]
				cost[s][t] = nx.shortest_path_length(G,source=s,target=t)
				G_new.add_edge(s, t, weight = cost[s][t])
	np.save('data/nodes.npy', np.array(nodelist))
	np.save('data/cost.npy', np.array(cost))
	nx.write_gml(G_new,"data/new_graph.gml")
	print "finish save data"
	return G_new,cost

def sQuest(filename,nodes,times,pt1):
	

	# =================================
	df = pd.read_csv('data/select_nodes.csv')
	select_df = df[df['pickup_nodes']!=df['dropoff_nodes']]
	print select_df.info()
	# =================================
	# quest = []
	# dropoff_dist,dropoff_ind = kdtree.query(dropoff_df,k=1)

	# if dist[0]<limit and dist[1]<limit:
	# 	print '=======',i,'=========='
	# 	print bnode,enode
	# 	print nodes[ind[0][0]],nodes[ind[1][0]]
	# 	count += 1
	# 	time1 = randint(pt1+1,pt1+300)
	# 	time2 = int(time1+5*randint(pt1,3*pt1))
	# 	quest.append([ind[0][0],time1,time2,ind[1][0]])
	# return quest

def sCars(num,limit,room):
	cars = []
	for i in range(num):
		lid = randint(0,limit)
		cars.append([lid,room])
	return cars


def pre_main_data():
	node_file = 'data/USA-road-d.NY.co'
	graph_file = 'data/USA-road-d.NY.gr'
	trip_file = 'data/trip_data_2.csv'
	nodes = sNodes(node_file)
	print "slect node num",len(nodes)
	nodelist = get_nodes_trip(trip_file,nodes)
	print len(nodelist)
	#=======================================================

	G,cost = sRoad(graph_file,nodelist)

	#======================================================
	# numQ = 0.1
	# pt =0.5
	# quest = sQuest(request_file,area,nodes,numQ,pt*60)
	# print quest
	# qlen = []
	# for numQ in [1,3,5,8,10]:
	# 	if numQ == 3:
	# 		for pt in [0,5,10,15]:
	# 			quest = sQuest(request_file,area,nodes,numQ,pt*60)
	# 			filename = 'data/'+str(numQ)+'.'+str(pt)+'-quests.npy'
	# 			np.save(filename, np.array(quest))
	# 	else:
	# 		quest = sQuest(request_file,area,nodes,numQ,300)
	# 		filename = 'data/'+str(numQ)+'.'+str(5)+'-quests.npy'
	# 		np.save(filename, np.array(quest))
	# print "generate quest"

	# for numC in [5,8,10,30,50]:
	# 	if numC == 10:
	# 		for roomC in [2,3,4,5]:
	# 			cars = sCars(numC*100,len(nodes),roomC)
	# 			filename = 'data/'+str(numC)+'.'+str(roomC)+'-cars.npy'
	# 			np.save(filename, np.array(cars))
	# 	else:
	# 		roomC = 3
	# 		cars = sCars(numC*100,len(nodes),roomC)
	# 		filename = 'data/'+str(numC)+'.'+str(roomC)+'-cars.npy'
	# 		np.save(filename, np.array(cars))
	# print "generate cars"

	# for numC in [5,8,10,30,50]:
	# 	if numC == 10:
	# 		for ql in [1,3,5,8,10]:
	# 			utility = [[random()/2+0.5 for i in range(numC*100)] for j in range(ql*1000)]
	# 			filename = 'data/'+str(ql)+'.'+str(numC)+'-utility.npy'
	# 			np.save(filename, np.array(utility))
	# 	else:
	# 		utility = [[random()/2+0.5 for i in range(numC*100)] for j in range(3000)]
	# 		filename = 'data/'+str(3)+'.'+str(numC)+'-utility.npy'
	# 		np.save(filename, np.array(utility))
	# print "generate utility"

if __name__ == '__main__':
	pre_main_data()
