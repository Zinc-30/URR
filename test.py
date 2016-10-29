def place(x):
	a = []
	a.append(x)
	return a


print place(4)

for i in range(3,0):
	print i
print len([1,2])
s = set()
s.add(2)
s.add(1)
print s
s.remove(1)
print s


x = 1 if [] else 0
print x


a =[1,2,3,4];
b = a;
a.append(5);
print b


print float('345')
def readRoad(filename,G):
	for line in open(filename):
		tmps = line.split(' ');
		if tmps[0] == 'a':
			G.add_edge(tmps[1], tmps[2], weight=float(tmps[3]))
	return G
import networkx as nx
G = nx.Graph()
G = readRoad('USA-road-t.BAY.gr',G)
print G.number_of_nodes()
