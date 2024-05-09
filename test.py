
class Algorithm:
    def fcfs(self, taskList):
        qu = []
        currentTask = '' 
        taskList = sorted(taskList, key=lambda x: x.arrivalTime)
        copyTL = taskList
        while taskList:
            counter = 0
            for task in taskList:
                currentTask = task.id
                currentTask
                task.timeExecuted.append(counter)
                for i in range(task.cpuBurst):
                    
                    counter += 1
                task.shift.append(counter) 
                taskList.pop(0)

        return self.gantPrinter(taskList)
    
    def gantPrinter(self,taskList):
        gantString = ""
        for task in taskList:
            taskString = f"|"
            for i in range(task.cpuBurst):
                if i == task.cpuBurst // 2:
                    taskString += f"{task.id}"
                taskString += "-"
            taskString += "|"
            gantString += taskString
        
        return gantString
    
        
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
    

class Task:
    tasks = []
    def __init__(self, id: str, arrivalTime: int, cpuBurst: int) -> None:
        self.id = id
        self.arrivalTime = arrivalTime
        self.cpuBurst = cpuBurst
        #time when executed can be 1 or many depending on the process
        #preemptive only has 1 non-preemptive has 1 or more
        self.timeExecuted = []
        #time shifted value can be 1 or more depending on the process 
        #preemptive only has 1 non-preemptive has 1 or more
        self.shift = []
        self.priority = 0

    def addTimeExecuted(self,T):
        self.timeExecuted.append(T)
        
    def addShift(self,T):
        self.shift.append(T)

    def __str__(self) -> str:
        return f"""ID: {self.id}
Arrival Time: {self.arrivalTime}
CPU Burst: {self.cpuBurst}
"""
    
    def __repr__(self) -> str:
        return self.__str__()


if __name__ == '__main__':
    tasks = []
    
    task1 = Task('A', 2, 8)
    task2 = Task('B', 0, 9)
    task3 = Task('C', 3, 12)
    task4 = Task('D', 5, 13)

    tasks.extend([task1,task2,task3,task4])
    algo = Algorithm()
    aUtil = algoUtil()

    fcfs_task = algo.fcfs(tasks)
    for task in tasks:
        print(task)
    print(fcfs_task)
