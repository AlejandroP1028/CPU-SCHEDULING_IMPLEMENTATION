#fcfs done
#spf in done


class algo_util:
    def get_total_burst(self,task_list):
        total_burst = 0
        for task in task_list:
            total_burst += task.cpu_burst
        return total_burst
    
    def task_waiting_time(self, time_executed,arrival_time):
        #waiting time = time executed - arrival time
        return time_executed - arrival_time
    
    def task_turnaround_time(self,time_of_completion,arrival_time):
        #time of completion - arrival time
        return time_of_completion - arrival_time

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
        self.time_executed: list[int] = []  # Time when executed can be 1 or many depending on the process
        self.shift: list[int] = []  # Time shifted value can be 1 or more depending on the process
        self.priority:int = 0
        self.waiting_time:int = 0
        self.turnaround_time:int = 0

    def __str__(self) -> str:
            return f"""ID: {self.id}
Arrival Time: {self.arrival_time}
CPU Burst: {self.cpu_burst}
CPU Burst Needed: {self.cpu_burst_needed}
Waiting Time: {self.waiting_time}
Turnaround Time: {self.turnaround_time}
"""

       
    
    def __repr__(self) -> str:
        return self.__str__()

class algo_printer:
    util = algo_util()
    def gant_printer(self,task_list: list[Task]):

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

    def turnaround_printer(self,task_list:list[Task]):
        turnaround_list = []
        turnaround_str = "Turnaround Time:\n"
        for task in task_list:
            turnaround_list.append(task.turnaround_time)
            turnaround_str += f"TA {task.id.lower()} = {task.turnaround_time}ms\n"

        turnaround_str += f"Average TA: {self.util.avg(turnaround_list)}ms"
        print(turnaround_str)

    def waiting_time_printer(self,task_list:list[Task]):
        waiting_time = []
        waiting_time_str = "Waiting Time:\n"
        for task in task_list:
            waiting_time.append(task.waiting_time)
            waiting_time_str += f"WT {task.id.lower()} = {task.waiting_time}ms\n"

        waiting_time_str += f"Average WT: {self.util.avg(waiting_time)}ms"
        print(waiting_time_str)
class Algorithm():
    printer = algo_printer()
    util = algo_util()

    def fcfs(self, task_list):
        counter = 0
        queue = []
        gant_string: str = ""
        current_task:Task = None
        finished_tasks = []
        task_list = sorted(task_list, key=lambda x: x.arrival_time)
        copy_task_list = task_list[:]

        while len(finished_tasks) != len(task_list):
            if copy_task_list:
                queue, copy_task_list = self.add_to_queue(copy_task_list, counter, queue)

            if queue:
                if self.check_first_in_q(queue, counter) and not current_task:
                    current_task = queue.pop(0)
                    current_task.time_executed.append(counter)
                    current_task.waiting_time = self.util.task_waiting_time(counter,current_task.arrival_time)
                    
            if current_task:
                
                gant_string += current_task.id
                current_task.cpu_burst_needed -= 1
                current_task, finished_tasks = self.process_finished_task(current_task, finished_tasks, counter)

            else:
                gant_string += "-"

            counter += 1  # Increment counter regardless of tasks
            
        print(gant_string)
        self.printer.gant_printer(finished_tasks)
        self.printer.turnaround_printer(finished_tasks)
        self.printer.waiting_time_printer(finished_tasks)
        #revert cpu burst needed

        self.revert_cpu_burst(task_list)
    def spf(self, task_list):
        counter = 0
        queue = []
        gant_string: str = ""
        current_task:Task = None
        finished_tasks = []
        task_list:list[Task] = sorted(task_list, key=lambda x: x.arrival_time)
        copy_task_list = task_list[:]

        while len(finished_tasks) != len(task_list) and counter < 50:

            #if there are still tasks in task list append it to queue if the first index of the task_list.arrival time == is equal to the counter
            if  copy_task_list:
                queue, copy_task_list = self.add_to_queue(copy_task_list,counter, queue)

            #if queue has tasks
            if queue:
                #check our current task
                #sort our queue by cpu burst
                queue = sorted(queue, key=lambda x: x.cpu_burst)

                #check first in q and if we dont have a current task if both are true
                if not current_task:
                    #current task will be the first in q then change task attributes
                    current_task = queue.pop(0)
                    current_task.time_executed.append(counter)
                    current_task.waiting_time = self.util.task_waiting_time(counter,current_task.arrival_time)

            
            if current_task:
                gant_string += current_task.id
                current_task.cpu_burst_needed -= 1
                current_task, finished_tasks = self.process_finished_task(current_task, finished_tasks, counter)

            else:
                gant_string += "-"

            counter += 1  # Increment counter regardless of tasks


        print(gant_string)
        self.printer.gant_printer(finished_tasks)
        self.printer.turnaround_printer(finished_tasks)
        self.printer.waiting_time_printer(finished_tasks)

        #revert cpu burst needed
        self.revert_cpu_burst(task_list)

    def revert_cpu_burst(self,task_list: list[Task]):
        for task in task_list:
            task.cpu_burst_needed = task.cpu_burst
            
    def add_to_queue(self, task_list: list[Task], counter, queue: list[Task]):
        if task_list[0].arrival_time == counter:
            task_list[0].time_executed.append(counter)
            queue.append(task_list[0])
            task_list.pop(0)
        return queue, task_list

    def check_first_in_q(self, queue: list[Task], counter):
        if queue and queue[0].arrival_time <= counter:
            return True
        return False
    
    def process_finished_task(self, current_task: Task, finished_tasks: list[Task], counter):
        if current_task.cpu_burst_needed == 0:
            current_task.shift.append(counter + 1)
            current_task.turnaround_time = self.util.task_turnaround_time(counter+1,current_task.arrival_time)
            finished_tasks.append(current_task)
            current_task = None

        return current_task, finished_tasks
    


if __name__ == '__main__':
    tasks = []
    
    task1 = Task('A', 0, 4)
    task2 = Task('B', 6, 2)
    task3 = Task('C', 7, 5)
    task4 = Task('D', 8, 14)
    task5 = Task('E', 9, 10)
    tasks.extend([task1,task2,task3,task4,task5])
    algo = Algorithm()

    algo.fcfs(tasks)
    algo.spf(tasks)
