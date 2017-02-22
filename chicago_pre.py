import networkx as nx
import numpy as np
import random
import pandas as pd
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
	nodes = []
	nodeid = []
	for line in open('chicago/chicago_points.csv','r'):
		tmps = line[:-1].split(',')
		nodeid.append(int(tmps[0]))
		nodes.append([int(tmps[1]),int(tmps[2])])
	return nodeid,nodes

def get_nodes_trip():
	select_df = pd.read_csv('chicago/trip.csv')
	print select_df.info()
	return set(select_df['x']) | set(select_df['y'])

def sRoad(limit,filename,nodes,ncores):
	# cost_file = 'data/old_cost.npy'
	# calc =======================
	if not os.path.exists('chicago/cost.npy'):
		G = nx.Graph()
		for line in open(filename,'r'):
			tmps = line[:-1].split(',')
			G.add_edge(int(tmps[0]), int(tmps[1]), weight = int(tmps[2]))
		print "generate into G.node num",len(G.nodes())
		print "generate into G.edges num",len(G.edges())
		pickle.dump(G, open('chicago/graph.txt', 'w'))
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
		# np.save('chicago/'+str(limit)+'_nodes.npy', np.array(nodelist))
		np.save('chicago/cost.npy', np.array(cost))
		print "finish save data"
	# read ==========================
	else:
		print 'read cost'
		cost = np.load('chicago/cost.npy').tolist()
	return cost

def sCars(num,room,nodes):
	cars = []
	for i in range(num):
		lid = random.sample(nodes,1)[0]
		cars.append([lid,room])
	np.save('chicago/'+str(num)+'.'+str(room)+'-cars.npy',np.array(cars))
	return cars
def sQuest(count,pt,eps,cost):
	# =================================
	df = pd.read_csv('chicago/CHICAGO_'+str(count)+'K_trips.csv')
	quest = []
	# =================================
	for rid in range(len(df)):
		bnode = int(df.iloc[rid][0])
		enode = int(df.iloc[rid][1])
		timec = rd.getCost(bnode,enode,cost)
		btime = random.randint(pt[0]*60,pt[1]*60)
		etime = btime + timec * eps
		# print bnode,enode,timec,cost[bnode][enode]
		quest.append([bnode,btime,etime,enode])
	np.save('chicago/'+str(count)+'.'+str(pt[0])+'.'+str(eps)+'-quests.npy',np.array(quest))

def pre_main_data():
	limit = 1000
	# node_file = 'chicago/chicago_points.csv'
	graph_file = 'chicago/chicago_roads.csv'
	# trip_file = 'chicago/2K_trips_chicago.csv'
	# request_file = 'data/50_select_nodes.csv'
	# print nodes
	nodes_set = get_nodes_trip()
	print "slect node num",len(nodes_set)
	#=======================================================
	cost = sRoad(limit,graph_file,nodes_set,1)
	#======================================================
	print 'doing riders'
	for count in [1,3]:
		for pt in [[1,10],[10,30],[30,60]]:
			sQuest(count,pt,1.5,cost)
	for eps in [1.2,1.7,2.0]:
		sQuest(3,[10,30],eps,cost)

	print 'doing cars'
	for count in [100,200,300,400,500]:
		sCars(count,3,nodes_set)
	for room in [2,4,5]:
		sCars(200,room,nodes_set)
	print 'doing utility'
	for ncars in [100,200,300,400,500]:
		for nquest in [1,3]:
			utility = [[random.random() for i in range(ncars)] for j in range(nquest*1000)]
			np.save('chicago/'+str(nquest)+'.'+str(ncars)+'-utility.npy',np.array(utility))
			
	print 'doing similarity'
	for nquest in [1,3]:
		for nquest in [1,3,5,8,10]:
			sim = [[random.random() for i in range(nquest*1000)] for j in range(nquest*1000)]
			np.save('chicago/'+str(nquest)+'.'+str(nquest)+'-sim.npy',np.array(sim))


if __name__ == '__main__':
	pre_main_data()
	# pre_toy_data()
