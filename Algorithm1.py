import copy
import readData as rd
class Algo1():
	
	def __init__(self,cost):
		if cost:
			self.cost = cost
		else:
			G = rd.readRoad()
			self.cost = rd.readCost()


	def getCost(self,x,y):
		if x in self.cost and y in self.cost[x]:
			return self.cost[x][y]
		else:
			return 1000000

	def insertEvent(self, Scopy, u, xplace, xtime,questId,pick):
		"""
		Scopy is original event list,
		u is the insert position
		{xplace,xtime,questId,pick} is event information
		"""
		S = copy.deepcopy(Scopy)
		event = S[u]
		S.remove(event)
		newevent1 = {'startLocation':event['startLocation'],'riders':set(event['riders']),'endLocation':xplace,'deadline':xtime}
		newevent2 = {'startLocation':xplace,'riders':set(event['riders']),'endLocation':event['endLocation'],'deadline':event['deadline']}
		S.insert(u,newevent1)
		S.insert(u+1,newevent2)
		if pick:
			for (i,x) in enumerate(S):
				if i>u:
					x['riders'].add(questId) 
		else:
			for (i,x) in enumerate(S):
				if i>u:
					x['riders'].remove(questId) 
		eTime = event['startTime'];
		for ei in range(u,len(S)):
			S[ei]['startTime']=eTime;
			eTime = eTime + self.getCost(S[ei]['startLocation'],S[ei]['endLocation'])
		tempTime = [x['deadline'] - x['startTime'] - self.getCost(x['startLocation'],x['endLocation']) for x in S];
		tempTime.reverse()
		fTime = tempTime[0]
		S.reverse()
		for i in range(len(S)):
			fTime = min(fTime,tempTime[i])
			if fTime<0:
				return [];
			S[i]['flexibleTime'] = fTime;
		S.reverse()
		return S

	def validEvents(self, S, xplace, xtime,avilabenum,pick,questId):
	    """
	    event = {'startLocation':,'startTime':,'flexibleTime':,'riders':(),'endLocation':,'deadline':} 
	    """
	    waitList=[]
	    for ei in range(len(S)):
	    	if pick and len(S[ei]['riders'])+1>avilabenum:
	    		continue
	    	if not pick and questId not in S[ei]['riders']:
	    		continue
	    	if ei>0 and S[ei]['startTime']>xtime:
	    		continue
	    	if self.getCost(S[ei]['startLocation'],xplace)> xtime:
	    		continue
	    	if self.getCost(S[ei]['startLocation'],xplace)+self.getCost(xplace,S[ei]['endLocation'])-self.getCost(S[ei]['startLocation'],S[ei]['endLocation'])>S[ei]['flexibleTime']:
	    		continue
	    	waitList.append((S[ei],self.getCost(S[ei]['startLocation'],xplace)+self.getCost(xplace,S[ei]['endLocation'])-self.getCost(S[ei]['startLocation'],S[ei]['endLocation']),ei))
		return waitList

	def ScheduleSingleRequest(self, S,car,request,questId):
		costIncreament = 100000;
		Sbest=[]
		eTime = 0
		if S == []: 
			event = {'startLocation':car[0],'riders':set(),'endLocation':request[0],'deadline':request[1]}
			event['startTime'] = eTime
			eTime = eTime + self.getCost(event['startLocation'],event['endLocation'])
			Sbest.append(event)
			event = {'startLocation':request[0],'riders':set([questId]),'endLocation':request[3],'deadline':request[2]}
			event['startTime'] = eTime
			eTime = eTime + self.getCost(event['startLocation'],event['endLocation'])
			Sbest.append(event)
			fTime = event['deadline'] - event['startTime'] - self.getCost(event['startLocation'],event['endLocation'])
			tempTime = [x['deadline'] - x['startTime'] - self.getCost(x['startLocation'],x['endLocation']) for x in Sbest];
			tempTime.reverse()
			Sbest.reverse()
			for i in range(len(Sbest)):
				fTime = min(fTime,tempTime[i])
				if fTime<0:
					return [];
				Sbest[i]['flexibleTime'] = fTime;
			Sbest.reverse()
			return Sbest
		else:
			waitPick = self.validEvents(S,request[0],request[1],car[1],1,questId)
			if not waitPick:
				return Sbest
			waitPick = sorted(waitPick, key=lambda e:e[1]);
			for pick in waitPick:
				if pick[1]>costIncreament:
					break
				if not self.insertEvent(S,pick[2],request[0],request[1],questId,1):
					continue
				tmpS = self.insertEvent(S,pick[2],request[0],request[1],questId,1)
				waitDrop = self.validEvents(tmpS,request[3],request[2],car[1],0,questId)
				if not waitDrop:
					break
				waitDrop = sorted(waitDrop, key=lambda e:e[1]);
				for drop in waitDrop:
					if pick[2]>drop[2]:
						continue
					if pick[1]+drop[1]>= costIncreament:
						break
					if self.insertEvent(tmpS,drop[2],request[3],request[2],questId,0):
						Sbest = self.insertEvent(tmpS,drop[2],request[3],request[2],questId,0)
						costIncreament = pick[1]+drop[1]
		return Sbest


# #input=




# # #output=


# print "2========="
# questId = 1;
# carId = 0;
# car = cars[carId];
# request = quests[questId];
# ScheduleSingleRequest(S,car,request,questId)
# print S

# print "3========="
# questId = 2;
# carId = 0;
# car = cars[carId];
# request = quests[questId];
# ScheduleSingleRequest(S,car,request,questId)
# print S

# print "4========="
# questId = 3;
# carId = 0;
# car = cars[carId];
# request = quests[questId];
# ScheduleSingleRequest(S,car,request,questId)
# print S



