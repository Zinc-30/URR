import networkx as nx
import readData as rd
import pickle
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
	def kShortestPathCpver(self,k,tf):
		C = set(self.G.nodes())
		for v in self.G.nodes():
			C.remove(v)
			for x in self.G.nodes():
				if x != v and x in tf[v] and len(tf[v][x])<=k:
					if set(tf[v][x]) & C:
						continue
					for y in self.G.nodes():
						if y!=v and y!=x and v in tf[y] and len(tf[y][v])<=k:
							if set(tf[y][v]) & C:
								continue
							if len(tf[v][x])+len(tf[y][v])>k:
								C.add(v)
		return C
	def areaConstruction(self,k):
		areaSet = [];
		tf = nx.shortest_path(self.G)
		kSpc = self.kShortestPathCpver(k,tf)
		# print kSpc
		area = {}
		radius = {}
		areadict = {}
		for u in kSpc:
			area[u] = set([u])
			areadict[u] = u
		for u in set(self.G.nodes())-kSpc:
			x = min([[self.getCost(u,v),v] for v in kSpc])
			area[x[1]].add(u)
			areadict[u] = x[1]
			if x[1] in radius:
				if self.getCost(x[1],u)>radius[x[1]]:
					radius[x[1]] = self.getCost(x[1],u)
			else:
				radius[x[1]] = self.getCost(x[1],u)
		filename = 'data/area-'+str(k)+'.txt'
		pickle.dump(area, open(filename, 'w'))
		filename = 'data/areadict-'+str(k)+'.npy'
		pickle.dump(areadict, open(filename, 'w'))
		filename = 'data/areaR-'+str(k)+'.npy'
		pickle.dump(radius, open(filename, 'w'))
		print 'write area data'
		print len(area)
                return area

# G = rd.readRoad()
# cost = rd.readCost()
# a5 = Algo5(G,cost)
# area = a5.areaConstruction(3)
# print area
