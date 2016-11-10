import readData as rd
from Algorithm1 import Algo1
import Algorithm2 as A2
import Algorithm3 as A3
import Algorithm6 as A6
from Algorithm5 import Algo5
from time import clock
import sys

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
	ans = a1.ScheduleSingleRequest(tmpS,car,request,questId)
	end = clock();
	time = end-start
	print "answer is ",ans
	print "time:", time
	return tmpS,time

def tA2():
	start = clock()
	ans = A2.bilateralArrangement(cost,cars,quests,utility,S)
	end = clock()
	time = end-start
	print "answer is ",ans
	print "time:", time
	return ans,time

def tA3():
	start = clock();
	ans = A3.efficiencyGreedy(cost,cars,quests,utility,S)
	end = clock();
	print "answer is ",ans
	print "time:", end-start
	return ans,end-start

def tA5(k):
	a5 = Algo5(G,cost)
	area = a5.areaConstruction(k)
	print "area is",area
	return area

def tA6(k):
	start = clock();
	ans = A6.groupScheduling(G,k,cost,cars,quests,utility,S)
	end = clock();
	print "answer is",ans
	print "time",end-start
	return ans,end-start



if len(sys.argv)<2:
	print "input num-th of Algorithm! eg: input 2"
else:
	print "test",sys.argv[1],"Algorithm"
	if sys.argv[1]=='1':
		if len(sys.argv)<4:
			print "in test 1: input requestid,carid"
		else:
			tA1(int(sys.argv[2]),int(sys.argv[3]))
	if sys.argv[1]=='5' or sys.argv[1]=='6':
		if len(sys.argv)<3:
			print "in test 5,6: input k of k-SPC"
		else:
			if sys.argv[1]=='6':
				tA6(int(sys.argv[2]))
			if sys.argv[1]=='5':
				tA5(int(sys.argv[2]))
	if sys.argv[1]=='2':
		tA2()
	if sys.argv[1]=='3':
		tA3()