    
class algoUtil:
    def getTotalBurst(self,taskList):
        totalBurst = 0
        for task in taskList:
            totalBurst += task.cpuBurst
        return totalBurst
    
    def taskWaitingTime(self, waitingT,arrivalT):
        #waiting time = waiting time - arrival time
        return waitingT - arrivalT
    
    def avg(self,list):
        num = 0
        for i in list:
            num += i
        return num/len(list)


if __name__ == '__main__':
    algo = algoUtil()
    task = [[8,3],[3,1],[2,1]]
    finalList = []
    for t in task:
        finalList.append(algo.taskWaitingTime(t[0],t[1]))
    
    print(algo.avg(finalList))
        


    