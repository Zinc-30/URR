import networkx as nx
G = nx.Graph()
G.add_weighted_edges_from([('A','B',1),('B','E',2),('E','H',1),('E','F',1),('F','H',2),('F','G',2),('G','H',3),('D','G',1),('A','D',2),('A','C',1),('C','F',5)])
cost = nx.shortest_path_length(G,weight='weight');

def areaConstruction(V,E,k):
	areaSet = [];

