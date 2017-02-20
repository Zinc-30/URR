import readData as rd
import pandas as pd
import numpy as np
import pickle
import Algorithm2 as A2
import Algorithm3 as A3
import Algorithm6 as A6
import baseline_cost
import baseline_utility
from time import clock
import os

def task(method,cost,quests,cars,utility,sim,paras,G,k):
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
	print "begin"
	start = clock()
	if method == 0:
		ans = A2.bilateralArrangement(cost,cars,quests,utility,S,sim,paras)
	elif method ==1:
		ans = A3.efficiencyGreedy(cost,cars,quests,utility,S,sim,paras)
	elif method ==2:
		areadict = getDict(k)
		radius = getRadius(k)
		ans = A6.groupScheduling(cost,cars,quests,utility,S,areadict,radius,paras)
	elif method ==3:
		ans = baseline_cost.costGreedy(cost,cars,quests,utility,S,sim,paras)
	elif method ==4:
		ans = baseline_utility.utilityGreedy(cost,cars,quests,utility,S,sim,paras)
	end = clock()
	time = end-start
	sum_u = rd.cal_u_all(ans,utility,sim,cost,quests,paras)
	print "=========method",method
	#print "answer is ",ans
	print "time:", time
	print "sum utility", sum_u
	return ans,time,sum_u

def test(cost,quests,cars,utility,sim,G,k,paras):
	# print "==============",numq,numc,pt,roomc,"============" 
	result = []
	# result.append([numq,numc,pt,roomc])
	for i in range(5):
		if i!=2:
			ans,time,sumu = task(i,cost,quests,cars,utility,sim,paras,G,k)
			result.append(time)
			result.append(sumu)
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

def test_toy():
	cost = np.load('toy_cost.npy').tolist()
	utility = np.load('toy_utility.npy').tolist()
	cars = np.load('toy_cars.npy').tolist()
	quests = np.load('toy_quests.npy').tolist()
	sim = np.load('toy_sim.npy').tolist()
	nquest = len(quests)
	ncars = len(cars)
	G=0
	k=0
	print nquest,ncars
	print test(cost,quests,cars,utility,sim,G,k,[0.5,0.3,0.2])
	print 'best',2.3301756318

if __name__ == "__main__":
	test_toy()
