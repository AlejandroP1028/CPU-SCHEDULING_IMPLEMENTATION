
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
    
if __name__ == '__main__':
    pass