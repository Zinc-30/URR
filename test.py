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
quests = rd.readQuests(3,5)
cars = rd.readCars(10,3)
utility = rd.readUtility(3,10)

def calsum(S):
    sum = 0;
    global utility
    for (i,tmps) in enumerate(S):
        riders = set()
	for x in tmps:
	    riders = riders|x['riders']
	for r in riders:
	    sum = sum + utility[r][i]
    return sum

def tA1(questId,carId):
	a1 = Algo1(cost)
	car = cars[carId]
	request = quests[questId]
	tmpS = S[carId]
	start = clock()
	ans = a1.ScheduleSingleRequest(tmpS,car,request,questId)
	end = clock();
	time = end-start
	#print "answer is ",ans
	print "time:", time
	return tmpS,time

def tA2():
	global utility
	global cost
	global quests
	global cars
	S = [[] for i in range(len(cars))]
	print "begin"
	start = clock()
	ans = A2.bilateralArrangement(cost,cars,quests,utility,S)
	end = clock()
	time = end-start
	sumu = calsum(ans)
	print "================A2================="
	#print "answer is ",ans
	print "time A2:", time
	print "sum utility", sumu
	return ans,time,sumu

def tA3():
	global utility
	global cost
	global quests
	global cars
	S = [[] for i in range(len(cars))]
	start = clock();
	ans = A3.efficiencyGreedy(cost,cars,quests,utility,S)
	end = clock();
	time = end-start
	sumu = calsum(ans)
	print "================A3================="
	#print "answer is ",ans
	print "time A3:", time
	print "sum utility", sumu
	return ans,time,sumu

def tA5(k):
	global cost
	global G
	a5 = Algo5(G,cost)
	area = a5.areaConstruction(k)
	#print "area is",area
	return area

def tA6(k):
	global utility
	global cost
	global quests
	global cars
	global G
	S = [[] for i in range(len(cars))]
	start = clock();
	ans = A6.groupScheduling(G,k,cost,cars,quests,utility,S)
	end = clock();
	time = end-start
	sumu = calsum(ans)
	print "================A6================="
	#print "answer is ",ans
	print "time A6:", time
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

def test(numq,numc,pt,roomc):
	print "==============",numq,numc,pt,roomc,"============" 
	result = []
	result.append([numq,numc,pt,roomc])
	# ans,time,sumu = tA2()
	# result.append([time,sumu])
	# ans,time,sumu = tA3()
	# result.append([time,sumu])
	ans,time,sumu = tA6(30)
	result.append([time,sumu])
	return result

if __name__ == "__main__":
	numq = 3
	numc = 10
	pt = 5
	roomc = 3
	result = []
	tA5(100)

#	for pt in [0,15,10,5]:
#		quests = rd.readQuests(3,pt)
#		result.append(test(numq,numc,pt,roomc))
	# numq = 3
	# numc = 10
	# pt = 5
	# roomc = 3	
	# for roomc in [2,5,4,3]:
	# 	cars = rd.readCars(10,roomc)
	# 	if roomc!=3:
	# 		result.append(test(numq,numc,pt,roomc))
	# numq = 3
	# numc = 10
	# pt = 5
	# roomc = 3
	# for numq in [1,5,8,10,3]:
	# 	quests = rd.readQuests(numq,5)
	# 	utility = rd.readUtility(numq,10)
	# 	if numq!=3:
	# 		result.append(test(numq,numc,pt,roomc))
	# numq = 3
	# numc = 10
	# pt = 5
	# roomc = 3
	# for numc in [5,8,50,30]:
	# 	utility = rd.readUtility(3,numc)
	# 	cars = rd.readCars(numc,3)
	# 	result.append(test(numq,numc,pt,roomc))
	# with open('data/result.txt','w') as f:
	# 	print >>f,"[#quests,#cars,range of pickup_time,car room],[time,sum utility]"
	# 	for r in result:
	# 		print >>f,result
