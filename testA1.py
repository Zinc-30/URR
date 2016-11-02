import SetInfo
import Algorithm1
from time import clock
G = SetInfo.G
cost = SetInfo.cost
quests = SetInfo.quests
cars = SetInfo.cars
utility = SetInfo.utility
questId = 0
carId = 0
car = cars[carId]
request = quests[questId]

S = []

start = clock();
S = Algorithm1.ScheduleSingleRequest(S,car,request,questId)
end = clock();
print "time:", end-start