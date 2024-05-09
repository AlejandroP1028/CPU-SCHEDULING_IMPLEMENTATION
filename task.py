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
    pass