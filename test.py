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
def getb(b):
	return b;
c = [getb(x) for x in b]
print c
a.append(5);
a.append([1,2,3])
print b


# print float('345')
# def readRoad(filename,G):
# 	for line in open(filename):
# 		tmps = line.split(' ');
# 		if tmps[0] == 'a':
# 			G.add_edge(tmps[1], tmps[2], weight=float(tmps[3]))
# 	return G
# import networkx as nx
# G = nx.Graph()
# G = readRoad('USA-road-t.BAY.gr',G)
# print G.number_of_nodes()

# import SetInfo
# import Algorithm1
# G = SetInfo.G
# cost = SetInfo.cost
# quests = SetInfo.quests
# cars = SetInfo.cars
# utility = SetInfo.utility
# questId = 0
# carId = 0
# car = cars[carId]
# request = quests[questId]

# S = []
# S = Algorithm1.ScheduleSingleRequest(S,car,request,questId)
# print S

# class x():
# 	cost = 'hah';
# 	def printc(self):
# 		print self.cost

# x1 = x()
# x1.printc()

# from Algorithm1 import getCost
# print getCost('1','24')
# from time import clock
# start = clock()