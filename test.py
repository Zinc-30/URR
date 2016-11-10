import readData as rd
from Algorithm1 import Algo1
import Algorithm2 as A2
import Algorithm3 as A3
from Algorithm5 import Algo5
from time import clock
G = rd.readRoad()
cost = rd.readCost()
quests = rd.readQuests()
cars = rd.readCars()
utility = rd.readUtility()
S = [[] for i in range(len(cars))]

def tA1(questId,carId):
	a1 = Algo1(cost)
	car = cars[carId]
	request = quests[questId]
	tmpS = S[carId]
	start = clock()
	tmpS = a1.ScheduleSingleRequest(tmpS,car,request,questId)
	end = clock();
	time = end-start
	print "answer is ",S
	print "time:", time
	return tmpS,time

def tA2():
	start = clock()
	S = A2.bilateralArrangement(cost,cars,quests,utility,S)
	end = clock()
	time = end-start
	print "answer is ",S
	print "time:", time
	return S,time

def tA3():
	start = clock();
	S = A3.efficiencyGreedy(cost,cars,quests,utility,S)
	end = clock();
	print "answer is ",S
	print "time:", 
	return S,end-start

def tA5(k):
	a5 = Algo5(G,cost)
	area = a5.areaConstruction(k)
	print "area is",area
	return area

def tA6(k):
	start = clock();
	S = A6.groupScheduling(G,k,cost,cars,quests,utility,S)
	end = clock();
	print "answer is",S
	print "time",end-start
	return S,end-start
