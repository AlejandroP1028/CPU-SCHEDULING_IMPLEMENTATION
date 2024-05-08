tasks = []

class Algorithm:
    def fcfs(self, taskList):
        taskList = sorted(taskList, key=lambda x: x.arrivalTime)
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

class Task:
    def __init__(self, id: str, arrivalTime: int, cpuBurst: int) -> None:
        self.id = id
        self.arrivalTime = arrivalTime
        self.cpuBurst = cpuBurst
        tasks.append(self)
        
    def __str__(self) -> str:
        return f"""ID: {self.id}
Arrival Time: {self.arrivalTime}
CPU Burst: {self.cpuBurst}
"""
    
    def __repr__(self) -> str:
        return self.__str__()

task1 = Task('A', 2, 8)
task2 = Task('B', 0, 9)
task3 = Task('C', 3, 12)
task4 = Task('D', 5, 13)

algo = Algorithm()
aUtil = algoUtil()

fcfs_task = algo.fcfs(tasks)
for task in tasks:
    print(task)
print(fcfs_task)
