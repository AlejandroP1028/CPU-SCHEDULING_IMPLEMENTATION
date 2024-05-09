
class Algorithm:
    def fcfs(self, task_list):
        counter = 0
        queue = []
        current_task = None
        finished_tasks = []
        task_list = sorted(task_list, key=lambda x: x.arrival_time)
        copy_task_list = task_list[:]

        while len(finished_tasks) != len(task_list):
            if copy_task_list:
                queue, copy_task_list = self.add_to_queue(copy_task_list, counter, queue)

            if queue:
                if self.check_current_task(queue, counter) and not current_task:
                    current_task = queue.pop(0)
                    current_task.time_executed = counter

            if current_task:
                current_task.cpu_burst_needed -= 1
                current_task, finished_tasks = self.check_finished_task(current_task, finished_tasks, counter)

            counter += 1  # Increment counter regardless of tasks

        print([task.id for task in finished_tasks])

        for task in finished_tasks:
            print(task)
        print([(task.id, task.cpu_burst) for task in task_list])

        self.gant_printer(task_list)

    def add_to_queue(self, task_list, counter, queue):
        if task_list[0].arrival_time == counter:
            task_list[0].time_executed = counter
            queue.append(task_list[0])
            task_list.pop(0)
        return queue, task_list

    def check_current_task(self, queue, counter):
        if queue and queue[0].arrival_time <= counter:
            return True
        return False

    def check_finished_task(self, current_task, finished_tasks, counter):
        if current_task.cpu_burst_needed == 0:
            current_task.shift.append(counter + 1)
            finished_tasks.append(current_task)
            current_task = None

        return current_task, finished_tasks


    def gant_printer(self,task_list):
        gant_string = ""
        for task in task_list:
            task_string = f"|"
            for i in range(task.cpu_burst):
                if i == task.cpu_burst // 2:
                    task_string += f"{task.id}"
                task_string += "-"
            task_string += "|"
            gant_string += task_string
        
        print(gant_string)
    
        
class algoUtil:
    def getTotalBurst(self,taskList):
        totalBurst = 0
        for task in taskList:
            totalBurst += task.cpu_burst
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

    def __init__(self, id: str, arrival_time: int, cpu_burst: int) -> None:
        self.id = id
        self.arrival_time = arrival_time
        self.cpu_burst = cpu_burst
        self.cpu_burst_needed = cpu_burst
        self.time_executed = []  # Time when executed can be 1 or many depending on the process
        self.shift = []  # Time shifted value can be 1 or more depending on the process
        self.priority = 0

    def add_time_executed(self, t):
        self.time_executed.append(t)

    def add_shift(self, t):
        self.shift.append(t)

    def __str__(self) -> str:
            return f"""ID: {self.id}
Arrival Time: {self.arrival_time}
CPU Burst: {self.cpu_burst}
CPU Burst Needed: {self.cpu_burst_needed}
Time Executed: {self.time_executed}
Time Shifted: {self.shift}
"""

       
    
    def __repr__(self) -> str:
        return self.__str__()


if __name__ == '__main__':
    tasks = []
    
    task1 = Task('A', 0, 8)
    task2 = Task('B', 3, 4)
    task3 = Task('C', 4, 5)
    task4 = Task('D', 6, 3)
    task5 = Task('E', 10, 2)

    tasks.extend([task1,task2,task3,task4,task5])
    algo = Algorithm()
    aUtil = algoUtil()

    algo.fcfs(tasks)
