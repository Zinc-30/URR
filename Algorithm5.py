import networkx as nx
import readData as rd
class Algo5():
	def __init__(self,G,cost):
		if G:
			self.G = G
		else:
			self.G = rd.readRoad()
		if cost:
			self.cost = cost
		else:
			self.cost = rd.readCost()
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
		filename = 'data/area-'+str(k)+'.txt'
		pickle.dump(area, open(filename, 'w'))
		print 'write area data'
		return area

# G = rd.readRoad()
# cost = rd.readCost()
# a5 = Algo5(G,cost)
# area = a5.areaConstruction(3)
# print area
