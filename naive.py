import numpy as np
from Algorithm1 import Algo1
import itertools
import copy
cost = np.load('toy_cost.npy').tolist()
utility = np.load('toy_utility.npy').tolist()
cars = np.load('toy_cars.npy').tolist()
quests = np.load('toy_quests.npy').tolist()
sim = np.load('toy_sim.npy').tolist()
nquest = len(quests)
ncars = len(cars)
a1 = Algo1(cost)
opt_ans = 0;
opt_S = [list() for i in range(ncars)]

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

def arrage(riders,rid,S,ans):
	global opt_ans
	global opt_S
	global ncars
	if rid==len(riders):
		ans = cal_u_all(S,utility,sim,cost,quests)
		if ans>opt_ans:
			opt_ans = ans
			opt_S = copy.deepcopy(S)
	else:
		for carid in range(ncars+1):
			if carid != ncars:
				tmps1=a1.ScheduleSingleRequest(S[carid],cars[carid],riders[rid],rid)
				if tmps1:
					# print "in change"
					copys = copy.deepcopy(S[carid])
					S[carid] = tmps1
					ans += 1
					arrage(riders,rid+1,S,ans)
					ans -= 1
					S[carid] = copys
			else:
				arrage(riders,rid+1,S,ans)
riderslist = list(itertools.permutations(quests,len(quests)))
print len(riderslist)
S = [list() for i in range(ncars)]
i = 0
for riders in riderslist:
	i += 1
	arrage(riders,0,S,0)
	# print 'opt_ans',opt_ans,i,opt_S
	# print opt_ans
print opt_ans,opt_S