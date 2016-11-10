import SetInfo
from Algorithm1 import Algo1
from time import clock
G = SetInfo.readRoad('road.txt')
cost = SetInfo.readCost(G)
quests = SetInfo.readQuests()
cars = SetInfo.readCars()
utility = SetInfo.readUtility()

a1 = Algo1(cost)
questId = 0
carId = 0
car = cars[carId]
request = quests[questId]
S = []
start = clock();
S = a1.ScheduleSingleRequest(S,car,request,questId)
end = clock();
print S
print "time:", end-start