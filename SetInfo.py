import networkx as nx
import copy
import os
import json
def readRoad(filename,G):
	if os.path.exists('graph.gml'):
		G = nx.read_gml("graph.gml")
	else:	
		for line in open(filename):
			tmps = line.split(' ');
			if tmps[0] == 'a':
				G.add_edge(tmps[1], tmps[2], weight=float(tmps[3]))
		nx.write_gml(G,"graph.gml")
	return G

G = nx.Graph()
G = readRoad('USA-road-t.BAY.gr',G)
cost = nx.shortest_path_length(G,weight='weight');
# quests = [['A',4,10,'H'],['F',7,10,'H'],['E',5,10,'G'],['G',2,7,'E']]
# cars = [['B',2,()],['D',2,()]] 
# utility = [[1,2],[3,2],[1,4],[5,1]]