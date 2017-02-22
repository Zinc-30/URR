import readData as rd
import pandas as pd
import numpy as np
import pickle
import Algorithm2 as A2
import Algorithm3 as A3
import Algorithm6 as A6
import Algorithm7 as A7
import baseline_cost
import baseline_utility
from time import clock
import os
import pp

def task(method,cost,quests,cars,utility,sim,paras,k):
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
		ans = A6.groupScheduling(cost,cars,quests,utility,S,areadict,radius,sim,paras)
	elif method ==3:
		areadict = getDict(k)
		radius = getRadius(k)
		ans = A7.groupScheduling(cost,cars,quests,utility,S,areadict,radius,sim,paras)
	elif method ==4:
		ans = baseline_cost.costGreedy(cost,cars,quests,utility,S,sim,paras)
	elif method ==5:
		ans = baseline_utility.utilityGreedy(cost,cars,quests,utility,S,sim,paras)
	end = clock()
	time = end-start
	sum_u = rd.cal_u_all(ans,utility,sim,cost,quests,paras)
	print "=========method",method
	#print "answer is ",ans
	print "time:", time
	print "sum utility", sum_u
	return ans,time,sum_u

def test(testname,cost,quests,cars,utility,sim,k,paras):
	# print "==============",numq,numc,pt,roomc,"============" 
	res = []
	for i in range(6):
		if i==3:
			ans,time,sumu = task(i,cost,quests,cars,utility,sim,paras,k)
			Riders = set()
			for s in ans:
				for x in s:
					Riders = Riders|x['riders']
			sum_r = len(Riders)
		else:
			sumu = 0
			time = 0
			sumu = 0
		res.append(time)
		res.append(sumu)
		res.append(sum_r)
	s = pd.Series(res,index = ['2-time','2-u','2-r','3-time','3-u','3-r','2+group-time','2+group-u','2+group-r',\
		'3+group-time','3+group-u','3+group-r''gt-time','gt-u','gt-r','gu-time','gu-u','gu-r'])
	s.to_csv('data/'+testname+'.csv')
	return testname,s

def test_main():
	result = pd.DataFrame([])
	cost = rd.readCost('data/50_cost.npy')
	ncores = 20
	jobs = []
	job_server = pp.Server(ncores)

	# test defult
	cars = rd.readCars(200,3)
	quests = rd.readQuests(3,10,1.5)
	utility = rd.readUtility(3,200)
	sim = rd.readSim(3,3)
	k = 10
	paras = [0.33,0.33]
	jobs.append(job_server.submit(test,('test-default',cost,quests,cars,utility,sim,k,paras),(task,),\
		('import os','from time import clock','import numpy as np','import pandas as pd','import readData as rd',\
			'import baseline_cost','import baseline_utility','import Algorithm2 as A2','import Algorithm3 as A3','import Algorithm6 as A6','import Algorithm7 as A7')))
	
	# test paras
	for paras in [[1,0],[0,0],[0,1]]:
		jobs.append(job_server.submit(test,('test-para='+str(paras),cost,quests,cars,utility,sim,k,paras),(task,),\
		('import os','from time import clock','import numpy as np','import pandas as pd','import readData as rd',\
			'import baseline_cost','import baseline_utility','import Algorithm2 as A2','import Algorithm3 as A3','import Algorithm6 as A6','import Algorithm7 as A7')))
	paras = [0.33,0.33]

	# test quest num
	for count in [1,5,8,10]:
		quests = rd.readQuests(count,10,1.5)
		utility = rd.readUtility(count,200)
		sim = rd.readSim(count,count)
		jobs.append(job_server.submit(test,('test-rider_num='+str(count),cost,quests,cars,utility,sim,k,paras),(task,),\
		('import os','from time import clock','import numpy as np','import pandas as pd','import readData as rd',\
			'import baseline_cost','import baseline_utility','import Algorithm2 as A2','import Algorithm3 as A3','import Algorithm6 as A6','import Algorithm7 as A7')))
	quests = rd.readQuests(3,10,1.5)
	utility = rd.readUtility(3,200)
	sim = rd.readSim(3,3)

	# test quest pt
	for pt in [[1,10],[30,60]]:
		quests = rd.readQuests(3,pt[0],1.5)
		jobs.append(job_server.submit(test,('test-rider_pt='+str(pt),cost,quests,cars,utility,sim,k,paras),(task,),\
		('import os','from time import clock','import numpy as np','import pandas as pd','import readData as rd',\
			'import baseline_cost','import baseline_utility','import Algorithm2 as A2','import Algorithm3 as A3','import Algorithm6 as A6','import Algorithm7 as A7')))

	# test quest eps
	for eps in [1.2,1.7,2.0]:
		quests = rd.readQuests(3,pt[0],1.5)
		jobs.append(job_server.submit(test,('test-rider_eps='+str(pt),cost,quests,cars,utility,sim,k,paras),(task,),\
		('import os','from time import clock','import numpy as np','import pandas as pd','import readData as rd',\
			'import baseline_cost','import baseline_utility','import Algorithm2 as A2','import Algorithm3 as A3','import Algorithm6 as A6','import Algorithm7 as A7')))


	# test car num
	for count in [100,300,400,500]:
		cars = rd.readCars(count,3)
		utility = rd.readUtility(3,count)
		jobs.append(job_server.submit(test,('test-car_num='+str(count),cost,quests,cars,utility,sim,k,paras),(task,),\
		('import os','from time import clock','import numpy as np','import pandas as pd','import readData as rd',\
			'import baseline_cost','import baseline_utility','import Algorithm2 as A2','import Algorithm3 as A3','import Algorithm6 as A6','import Algorithm7 as A7')))
	cars = rd.readCars(200,3)
	utility = rd.readUtility(3,200)	

	# test car room
	for room in [2,4,5]:
		cars = rd.readCars(200,room)
		jobs.append(job_server.submit(test,('test-car_room='+str(room),cost,quests,cars,utility,sim,k,paras),(task,),\
		('import os','from time import clock','import numpy as np','import pandas as pd','import readData as rd',\
			'import baseline_cost','import baseline_utility','import Algorithm2 as A2','import Algorithm3 as A3','import Algorithm6 as A6','import Algorithm7 as A7')))

	for job in jobs:
		job_name,job_ans = job()
		result[job_name] = job_ans
	result.to_csv('data/result.csv')

def test_toy():
	cost = np.load('toy_cost.npy').tolist()
	utility = np.load('toy_utility.npy').tolist()
	cars = np.load('toy_cars.npy').tolist()
	quests = np.load('toy_quests.npy').tolist()
	sim = np.load('toy_sim.npy').tolist()
	nquest = len(quests)
	ncars = len(cars)
	k = 3
	print nquest,ncars
	print test('toy',cost,quests,cars,utility,sim,k,[0.3,0.3])
	print 'best',1.86218116608

if __name__ == "__main__":
	# test_toy()
	test_main()
