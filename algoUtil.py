    
class algoUtil:
    def getTotalBurst(self,taskList):
        totalBurst = 0
        for task in taskList:
            totalBurst += task.cpuBurst
        return totalBurst
    
if __name__ == '__main__':
    pass