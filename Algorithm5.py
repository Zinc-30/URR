import networkx as nx
import SetInfo
class Algo5():
	def __init__(self,G,cost):
		if G:
			self.G = G
		else:
			self.G = SetInfo.readRoad('road.txt')
		if cost:
			self.cost = cost
		else:
			self.cost = SetInfo.readCost(self.G)

# G = nx.Graph()
# G.add_weighted_edges_from([('A','B',1),('B','E',2),('E','H',1),('E','F',1),('F','H',2),('F','G',2),('G','H',3),('D','G',1),('A','D',2),('A','C',1),('C','F',5)])
# cost = nx.shortest_path_length(G,weight='weight');

	def getCost(self,x,y):
		if x in self.cost and y in self.cost[x]:
			return self.cost[x][y]
		else:
			return 1000000


	def kShortestPathCpver(self,k):
		C = set(self.G.nodes())
		for v in self.G.nodes():
			C.remove(v)
			tf = nx.shortest_path(self.G,source=v)
			for x in self.G.nodes():
				if x != v and x in tf and len(tf[x])<=k:
					if set(tf[x]) & C:
						continue
					for y in self.G.nodes():
						if y!=v and y!=x and y in tf and len(tf[y])<=k:
							if set(tf[y]) & C:
								continue
							if len(tf[x])+len(tf[y])>k:
								C.add(v)
		return C


	def areaConstruction(self,k):
		areaSet = [];
		kSpc = self.kShortestPathCpver(k)
		# print kSpc
		area = {}
		for u in kSpc:
			area[u] = set([u])
		for u in set(self.G.nodes())-kSpc:
			x = min([[self.getCost(u,v),v] for v in kSpc])
			area[x[1]].add(u);
		return area

# G = SetInfo.readRoad('road.txt')
# cost = SetInfo.readCost(G)
# a5 = Algo5(G,cost)
# area = a5.areaConstruction(3)
# print area
