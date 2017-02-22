import networkx as nx
import numpy as np
import random
import pandas as pd
from sklearn.neighbors import KDTree
import pp
import os
import pickle
import readData as rd
def calcost(G,subl,wl):
	cost = dict()
	for s in subl:
		cost[s] = {}
		for t in wl:
			cost[s][t] = nx.astar_path_length(G,source=s,target=t,weight='weight')
	return cost
def sNodes(filename):
	i = 0
	nodes = []
	for line in open(filename,'r'):
		tmps = line[:-1].split(' ')
		i = i + 1
		if tmps[0] == 'v':
			nodes.append([int(tmps[2]),int(tmps[3])])
	return nodes
def get_nodes_trip(limit,filename,nodes):
	if not os.path.exists('data/'+str(limit)+'_select_nodes.csv'):
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
		nodesh = np.logical_and(pickup_ind>132000,dropoff_ind>132000)
		select_flag = np.logical_and(select_flag,nodesh)
		select_df = pd.DataFrame()
		select_df['pickup_nodes'] = pickup_ind[select_flag]
		select_df['dropoff_nodes'] = dropoff_ind[select_flag]
		select_df['cost'] = np.array(df['trip_time_in_secs'])[select_flag.T[0]]
		print 'purn data and write'
		select_df = select_df[select_df['pickup_nodes']!=select_df['dropoff_nodes']]
		select_df.to_csv('data/'+str(limit)+'_select_nodes.csv')
		print select_df.info()
	else:
	# read ==============================
		select_df = pd.read_csv('data/'+str(limit)+'_select_nodes.csv')
		print select_df.info()
	return set(select_df['pickup_nodes']) | set(select_df['dropoff_nodes'])

def sRoad(limit,filename,nodes,ncores):
	# cost_file = 'data/old_cost.npy'
	# calc =======================
	if not os.path.exists('data/'+str(limit)+'_cost.npy'):
		G = nx.Graph()
		for line in open(filename,'r'):
			tmps = line[:-1].split(' ')
			if tmps[0] == 'a' and int(tmps[1])>132000 and int(tmps[2])>132000:
				G.add_edge(int(tmps[1]), int(tmps[2]), weight = int(tmps[3]))
		print "generate into G.node num",len(G.nodes())
		print "generate into G.edges num",len(G.edges())
		pickle.dump(G, open('data/'+str(limit)+'_graph.txt', 'w'))
		nodelist = list(nodes)
		nodelist.sort()
		cost = dict()
		print "calc cost distance between nodes",len(nodelist)
			# ++++=pp-version =========
		if ncores>1:
			jobs = []
		 	job_server = pp.Server(ncores)
		 	inter = len(nodelist)/ncores
		 	for ni in range(ncores):
		 		subl = nodelist[ni*inter:(ni+1)*inter]
		 		jobs.append(job_server.submit(calcost,(G,subl,nodelist),(),("import networkx as nx",)))
		 	jobs.append(job_server.submit(calcost,(G,nodelist[ncores*inter:],nodelist),(),("import networkx as nx",)))
		 	job_server.wait()
		 	for job in jobs:
		 		job_ans = job()
		 		cost.update(job_ans)
		else:
			# ++++=1s-version ========
			for i in range(len(nodelist)):
				s = nodelist[i]
				if i%10==0:
					print 'doing',s,i,'/',len(nodelist)
				if s not in cost:
					cost[s] = {}
				for j in range(len(nodelist)):
					t = nodelist[j]
					if t not in cost[s]:
						cost[s][t] = nx.astar_path_length(G,source=s,target=t,weight='weight')
						if t not in cost:
							cost[t] = {}
						cost[t][s] = cost[s][t]
			#===save data==========
		np.save('data/'+str(limit)+'_nodes.npy', np.array(nodelist))
		np.save('data/'+str(limit)+'_cost.npy', np.array(cost))
		print "finish save data"
	# read ==========================
	else:
		print 'read cost'
		cost = np.load('data/'+str(limit)+'_cost.npy').tolist()
	return cost

def sCars(num,room,nodes):
	cars = []
	for i in range(num):
		lid = random.sample(nodes,1)[0]
		cars.append([lid,room])
	np.save('data/'+str(num)+'.'+str(room)+'-cars.npy',np.array(cars))
	return cars
def sQuest(count,pt,eps,cost):
	# =================================
	df = pd.read_csv('data/'+str(count)+'K_trips.csv')
	quest = []
	# =================================
	for rid in range(len(df)):
		bnode = int(df.iloc[rid][0])
		enode = int(df.iloc[rid][1])
		timec = rd.getCost(bnode,enode,cost)
		btime = random.randint(pt[0]*5,pt[1]*5)
		etime = btime + timec * eps
		# print bnode,enode,timec,cost[bnode][enode]
		quest.append([bnode,btime,etime,enode])
	np.save('data/'+str(count)+'.'+str(pt[0])+'.'+str(eps)+'-quests.npy',np.array(quest))

def pre_main_data():
	limit = 50
	node_file = 'data/USA-road-d.NY.co'
	graph_file = 'data/USA-road-d.NY.gr'
	trip_file = 'data/trip_data_2.csv'
	# request_file = 'data/50_select_nodes.csv'
	nodes = sNodes(node_file)
	nodes_set = get_nodes_trip(limit,trip_file,nodes)
	print "slect node num",len(nodes_set)
	#=======================================================
	cost = sRoad(limit,graph_file,nodes_set,1)
	#======================================================
	print 'doing riders'
	pt = [10,30]
	for count in [1,3,5,8,10]:
		sQuest(count,pt,1.5,cost)
	for pt in [[10,30],[30,60]]:
		sQuest(3,pt,1.5,cost)

	for eps in [1.2,1.7,2.0]:
		sQuest(3,[10,30],eps,cost)

	# print 'doing cars'
	# for count in [100,200,300,400,500]:
	# 	for room in [2,3,4,5]:
	# 		sCars(count,room,nodes_set)
	# print 'doing utility'
	# for ncars in [100,200,300,400,500]:
	# 	for nquest in [1,3,5,8,10]:
	# 		utility = [[random.random() for i in range(ncars)] for j in range(nquest*1000)]
	# 		np.save('data/'+str(nquest)+'.'+str(ncars)+'-utility.npy',np.array(utility))
			
	# print 'doing similarity'
	# for nquest in [1,3,5,8,10]:
	# 	for nquest in [1,3,5,8,10]:
	# 		sim = [[random.random() for i in range(nquest*1000)] for j in range(nquest*1000)]
	# 		np.save('data/'+str(nquest)+'.'+str(nquest)+'-sim.npy',np.array(sim))


def pre_toy_data():
	nquest = 6
	ncars = 3
	G = nx.Graph()
	for i in range(40):
		if i%5!= 4:
			G.add_edge(i,i+1,weight = 1)
			G.add_edge(i+1,i,weight = 1)
		G.add_edge(i,i+5,weight = 1)
		G.add_edge(i+5,i,weight = 1)
	cost = nx.shortest_path_length(G)
	cars = []
	for i in range(ncars):
		cars.append([random.randint(i,i+3)*5,3])
	quests = []
	for i in range(nquest):
		quests.append([i,3,10,i+11])
	utility = [[random.random() for i in range(ncars)] for j in range(nquest)]
	sim = [[random.random() for i in range(len(quests))] for j in range(len(quests))]
	np.save('toy_cost.npy',np.array(cost))
	np.save('toy_utility.npy',np.array(utility))
	np.save('toy_cars.npy',np.array(cars))
	np.save('toy_quests.npy',np.array(quests))
	np.save('toy_sim.npy',np.array(sim))

if __name__ == '__main__':
	pre_main_data()
	# pre_toy_data()
