import networkx as nx
import numpy as np
import random
import pandas as pd
from sklearn.neighbors import KDTree
import pp
import os
def calcost(G,subl,wl):
	cost = dict()
	for s in subl:
		cost[s] = {}
	 	print 'doing',s
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
			node = [int(tmps[2]),int(tmps[3])]
			nodes.append([node[0],node[1]])
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
		select_df = pd.DataFrame()
		select_df['pickup_nodes'] = pickup_ind[select_flag]
		select_df['dropoff_nodes'] = dropoff_ind[select_flag]
		select_df['cost'] = np.array(df['trip_time_in_secs'])[select_flag.T[0]]
		print select_df.info()	
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
	G = nx.Graph()
	for line in open(filename,'r'):
		tmps = line[:-1].split(' ')
		if tmps[0] == 'a':
			G.add_edge(int(tmps[1]), int(tmps[2]), weight = int(tmps[3]))
	print "generate into G.node num",len(G.nodes())
	print "generate into G.edges num",len(G.edges())
	nx.write_gml(G,'data/'+str(limit)+'_graph.gml')
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
	# cost = np.load(cost_file).tolist()
	# G_new = nx.read_gml("data/new_graph.gml")
	return G,cost
def sCars(num,nodes,room):
	cars = []
	for i in range(num):
		lid = random.sample(nodes,1)[0]
		cars.append([lid,room])
	return cars
def sQuest(filename,count,pt,cost):
	# =================================
	df = pd.read_csv(filename)
	select_df = df[df['pickup_nodes']!=df['dropoff_nodes']]
	print select_df.info()
	# =================================
	quest = []
	for i in range(count*10):
		rid = random.randint(0,len(df))
		bnode = select_df.iloc[rid]['pickup_nodes']
		enode = select_df.iloc[rid]['dropoff_nodes']
		timec = select_df.iloc[rid]['cost']
		btime = random.randint(pt,pt+300)
		etime = btime + timec
		print bnode,enode,timec,cost[bnode][enode]
		quest.append([bnode,btime,etime,enode])
	print quest

def pre_main_data():
	limit = 30
	node_file = 'data/USA-road-d.NY.co'
	graph_file = 'data/USA-road-t.NY.gr'
	trip_file = 'data/trip_data_2.csv'
	request_file = 'data/50_select_nodes.csv'
	nodes = sNodes(node_file)
	nodes_set = get_nodes_trip(limit,trip_file,nodes)
	print "slect node num",len(nodes_set)
	#=======================================================
	G,cost = sRoad(limit,graph_file,nodes_set,4)
	#======================================================
	# numQ = 1
	# pt =0.5
	# quest = sQuest(request_file,numQ,pt*60,cost)
	# print quest
	# qlen = []
	# for numQ in [1,2,3,4,5]:
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

def pre_toy_data():
	nquest = 8
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
