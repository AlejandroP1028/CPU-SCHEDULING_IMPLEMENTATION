class Task:
    tasks = []
    def __init__(self, id: str, arrivalTime: int, cpuBurst: int) -> None:
        self.id = id
        self.arrivalTime = arrivalTime
        self.cpuBurst = cpuBurst
        
    def __str__(self) -> str:
        return f"""ID: {self.id}
Arrival Time: {self.arrivalTime}
CPU Burst: {self.cpuBurst}
"""
    
    def __repr__(self) -> str:
        return self.__str__()
    
if __name__ == '__main__':