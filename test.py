import readData as rd
import pandas as pd
import numpy as np
import pickle
from Algorithm1 import Algo1
import Algorithm2 as A2
import Algorithm3 as A3
import Algorithm6 as A6
from Algorithm5 import Algo5

import baseline_cost
import baseline_utility

from time import clock
import os

def getCost(x,y,cost):
	if x in cost and y in cost[x]:
		return cost[x][y]
	else:
		return 1000000

def calCost(S,cost):
	costTime = 0;
	for x in S:
		costTime = costTime + getCost(x['startLocation'],x['endLocation'],cost)
	return costTime

def cal_u(cid,rid,S,s1,t1,utility,sim,cost):
	u1 = utility[rid][cid]
	cost_all = calCost(S,cost)
	u2 = 0
	cost_sum = 0
	for x in S:
		if rid in x['riders']:
			cost_x = getCost(x['startLocation'],x['endLocation'],cost)
			rate = cost_x/cost_all
			for r in x['riders']:
				if r!=rid:
					u2 += rate/(len(x['riders'])-1)*sim[r][rid]
			cost_sum += cost_x
	u3 = 2/(1+np.exp(cost_sum/getCost(s1,t1,cost)))
	return u1*0.5+u2*0.3+u3*0.2

def cal_u_car(cid,S,utility,sim,cost,quests):
	riders = set([])
	for x in S:
		riders = riders | x['riders']
	sum_u = 0	
	for rid in riders:
		sum_u += cal_u(cid,rid,S,quests[rid][0],quests[rid][3],utility,sim,cost)
	return sum_u

def cal_u_all(S,utility,sim,cost,quests):
	ans = 0
	for i in range(len(S)):
		ans += cal_u_car(i,S[i],utility,sim,cost,quests)
	return ans

def calsum(S,utility):
    sum = 0;
    for (i,tmps) in enumerate(S):
        riders = set()
	for x in tmps:
	    riders = riders|x['riders']
	for r in riders:
	    sum = sum + utility[r][i]
    return sum

def tA1(questId,carId,cost,cars,quests,S):
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

def tA2(cost,quests,cars,utility,sim):
	S = [[] for i in range(len(cars))]
	print cars
	print "begin"
	start = clock()
	ans = A2.bilateralArrangement(cost,cars,quests,utility,S,sim)
	end = clock()
	time = end-start
	sumu = cal_u_all(ans,utility,sim,cost,quests)
	print "================A2================="
	#print "answer is ",ans
	print "time A2:", time
	print "sum utility", sumu
	return ans,time,sumu

def tA3(cost,quests,cars,utility,sim):
	S = [[] for i in range(len(cars))]
	start = clock();
	ans = A3.efficiencyGreedy(cost,cars,quests,utility,S,sim)
	end = clock();
	time = end-start
	sumu = cal_u_all(ans,utility,sim,cost,quests)
	print "================A3================="
	#print "answer is ",ans
	print "time A3:", time
	print "sum utility", sumu
	return ans,time,sumu

def tA5(k,cost,G):
	a5 = Algo5(G,cost)
	area = a5.areaConstruction(k)
	#print "area is",area
	return area

def tA6(cost,quests,cars,utility,sim,G,k):
	def getArea(G,k,cost):
		filename = 'data/area-'+str(k)+'.txt'
		if os.path.exists(filename):
			area = pickle.load(open(filename, 'r'))
			print 'get area data'
		else:
			a5 = Algo5(G,cost)
			area = a5.areaConstruction(k)
			pickle.dump(area, open(filename, 'w'))
			print 'write area data'
		return area
	def getDict(k):
		filename = 'data/areadict-'+str(k)+'.npy'
		if os.path.exists(filename):
			print 'read dict data'
			return pickle.load(open(filename, 'r'))
		else:
			print 'no dict data'
	def getRadius(k):
		filename = 'data/areaR-'+str(k)+'.npy'
		if os.path.exists(filename):
			print 'read radic data'
			return pickle.load(open(filename, 'r'))
		else:
			print 'no dict data'
	S = [[] for i in range(len(cars))]
	getArea(G,k,cost)
	areadict = getDict(k)
	radius = getRadius(k)
	# =======================
	start = clock();
	ans = A6.groupScheduling(cost,cars,quests,utility,S,areadict,radius)
	end = clock();
	time = end-start
	sumu = cal_u_all(ans,utility,sim,cost,quests)
	print "================A6================="
	#print "answer is ",ans
	print "time A6:", time
	print "sum utility", sumu
	return ans,time,sumu

def tbase1(cost,quests,cars,utility,sim):
	S = [[] for i in range(len(cars))]
	start = clock();
	ans = baseline_cost.costGreedy(cost,cars,quests,utility,S,sim)
	end = clock();
	time = end-start
	sumu = cal_u_all(ans,utility,sim,cost,quests)
	print "================costGreedy================="
	#print "answer is ",ans
	print "time tbase1:", time
	print "sum utility", sumu
	return ans,time,sumu
def tbase2(cost,quests,cars,utility,sim):
	S = [[] for i in range(len(cars))]
	start = clock();
	ans = baseline_utility.utilityGreedy(cost,cars,quests,utility,S,sim)
	end = clock();
	time = end-start
	sumu = cal_u_all(ans,utility,sim,cost,quests)
	print "================utilitybGreedy================="
	#print "answer is ",ans
	print "time tbase2:", time
	print "sum utility", sumu
	return ans,time,sumu
# if len(sys.argv)<2:
# 	print "input num-th of Algorithm! eg: input 2"
# else:
# 	print "test",sys.argv[1],"Algorithm"
# 	if sys.argv[1]=='1':
# 		if len(sys.argv)<4:
# 			print "in test 1: input requestid,carid"
# 		else:
# 			tA1(int(sys.argv[2]),int(sys.argv[3]))
# 	if sys.argv[1]=='5' or sys.argv[1]=='6':
# 		if len(sys.argv)<3:
# 			print "in test 5,6: input k of k-SPC"
# 		else:
# 			if sys.argv[1]=='6':
# 				tA6(int(sys.argv[2]))
# 			if sys.argv[1]=='5':
# 				tA5(int(sys.argv[2]))
# 	if sys.argv[1]=='2':
# 		tA2()
# 	if sys.argv[1]=='3':
# 		tA3()

def test(cost,quests,cars,utility,sim,G,k):
	# print "==============",numq,numc,pt,roomc,"============" 
	result = []
	# result.append([numq,numc,pt,roomc])
	ans,time,sumu = tA2(cost,quests,cars,utility,sim)
	result.append(time)
	result.append(sumu)
	# print ans
	ans,time,sumu = tA3(cost,quests,cars,utility,sim)
	result.append(time)
	result.append(sumu)
	ans,time,sumu = tbase1(cost,quests,cars,utility,sim)
	result.append(time)
	result.append(sumu)	
	ans,time,sumu = tbase2(cost,quests,cars,utility,sim)
	result.append(time)
	result.append(sumu)
	# ans,time,sumu = tA6(cost,quests,cars,utility,sim,G,k)
	# result.append(time)
	# result.append(sumu)
	return result

def test_main():
	G = rd.readRoad()
	cost = rd.readCost()
	quests = rd.readQuests(3,5)
	cars = rd.readCars(10,3)
	utility = rd.readUtility(3,10)
	# finish read data
	numq = 3
	numc = 10
	pt = 5
	roomc = 3
	result = pd.DataFrame([],columns=['2-time','2-sumu','3-time','3-sumu','6-time','6-sumu'])
	# tA5(30)
	for pt in [0,10,5]:
		quests = rd.readQuests(3,pt)
		result.append(test(numq,numc,pt,roomc))
	numq = 3
	numc = 10
	pt = 5
	roomc = 3	
	for roomc in [2,5,4,3]:
		cars = rd.readCars(10,roomc)
		if roomc!=3:
			result.append(test(numq,numc,pt,roomc))
	numq = 3
	numc = 10
	pt = 5
	roomc = 3
	for numq in [1,5,8,10,3]:
		quests = rd.readQuests(numq,5)
		utility = rd.readUtility(numq,10)
		if numq!=3:
			result.append(test(numq,numc,pt,roomc))
	numq = 3
	numc = 10
	pt = 5
	roomc = 3
	for numc in [5,8,50,30]:
		utility = rd.readUtility(3,numc)
		cars = rd.readCars(numc,3)
		result.append(test(numq,numc,pt,roomc))
	with open('data/result.txt','w') as f:
		print >>f,"[#quests,#cars,range of pickup_time,car room],[time,sum utility]"
		for r in result:
			print >>f,result

def test_toy():
	cost = np.load('toy_cost.npy').tolist()
	utility = np.load('toy_utility.npy').tolist()
	cars = np.load('toy_cars.npy').tolist()
	quests = np.load('toy_quests.npy').tolist()
	sim = [[1 for i in range(len(quests))] for j in range(len(quests))]
	G=0
	k=0
	print test(cost,quests,cars,utility,sim,G,k)

if __name__ == "__main__":
	test_toy()
