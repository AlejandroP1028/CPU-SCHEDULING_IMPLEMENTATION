# bug 1: if arrival time of multiple tasks is the same only one will go into the queue resulting in an infinite loop
# solution: change add_to_queue implementation to not check for only one task but loop through all the tasks in the task list
# status: resolved

# bug 2: if id of task is more than 1 the printer would go wild
# solution: limit id of task to 1 character
# status: resolved

# bug 3: if number of tasks is 0 the program continues
# solution : add an error handler to improve
# status : not yet resolved 

#bug 4: if the input for arrival time is not an integer there will be Value Error
#solution: add try catch for value error in arrival time input
#status : not yet resolved.

class algo_util:
    def get_total_burst(self, task_list):
        total_burst = 0
        for task in task_list:
            total_burst += task.cpu_burst
        return total_burst

    def task_waiting_time(self, time_executed, arrival_time):
        # waiting time = time executed - arrival time
        return time_executed - arrival_time

    def task_turnaround_time(self, time_of_completion, arrival_time):
        # time of completion - arrival time
        return time_of_completion - arrival_time

    def avg(self, lst):
        num = 0
        for i in lst:
            num += i
        return num / len(lst)


class Task:
    tasks = []

    def __init__(self, id: str, arrival_time: int, cpu_burst: int) -> None:
        if len(id) != 1:
            raise ValueError("Task ID must be a single character.")
        if self.check_id_exists(id):
            raise ValueError("Task ID must be unique.")
        self.id = id
        self.arrival_time = arrival_time
        self.cpu_burst = cpu_burst
        self.cpu_burst_needed = cpu_burst
        self.waiting_time: int = 0
        self.turnaround_time: int = 0
        self.time_executed: list[int] = []  # Time when executed can be 1 or many depending on the process
        self.shift: list[int] = []  # Time shifted value can be 1 or more depending on the process
        Task.tasks.append(self)

    @staticmethod
    def check_id_exists(id: str) -> bool:
        for task in Task.tasks:
            if task.id == id:
                return True
        return False

    def __str__(self) -> str:
        return f"""ID: {self.id}
Arrival Time: {self.arrival_time}
CPU Burst: {self.cpu_burst}
CPU Burst Needed: {self.cpu_burst_needed}
Waiting Time: {self.waiting_time}
Turnaround Time: {self.turnaround_time}
Time Executed: {self.time_executed}
Time Shifted: {self.shift}
"""

    def __repr__(self) -> str:
        return self.__str__()


class algo_printer:
    util = algo_util()

    def gant_printer(self, gant_string):
        final_string = ""
        str_list = [char for char in gant_string]
        current_char = None
        current_char_count = 0

        for char in str_list:
            if current_char == char:
                current_char_count += 1
            else:
                if current_char:
                    final_string += "|"
                    for x in range(current_char_count):
                        if x == current_char_count // 2:
                            if current_char == "-":
                                final_string += "@"
                            else:
                                final_string += current_char
                        else:
                            if current_char == "-":
                                final_string += "@"
                            else:
                                final_string += "-"
                    current_char_count = 0  # Reset count for the new character

                current_char = char
                current_char_count = 1

        # Append the remaining characters after the loop ends
        if current_char:
            final_string += "|"
            for x in range(current_char_count):
                if x == current_char_count // 2:
                    final_string += current_char
                else:
                    if current_char == "-":
                        final_string += " "
                    else:
                        final_string += "-"

        final_string += "|"
        print(final_string)

    def turnaround_printer(self, task_list: list[Task]):
        turnaround_list = []
        turnaround_str = "Turnaround Time:\n"
        for task in task_list:
            turnaround_list.append(task.turnaround_time)
            turnaround_str += f"TA {task.id.lower()} = {task.turnaround_time}ms\n"

        turnaround_str += f"Average TA: {self.util.avg(turnaround_list)}ms"
        print(turnaround_str)

    def waiting_time_printer(self, task_list: list[Task]):
        waiting_time = []
        waiting_time_str = "Waiting Time:\n"
        for task in task_list:
            waiting_time.append(task.waiting_time)
            waiting_time_str += f"WT {task.id.lower()} = {task.waiting_time}ms\n"

        waiting_time_str += f"Average WT: {self.util.avg(waiting_time)}ms"
        print(waiting_time_str)


class Algorithm:
    printer = algo_printer()
    util = algo_util()

    def fcfs(self, task_list):
        counter = 0
        queue = []
        gant_string: str = ""
        current_task: Task = None
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
                    current_task.waiting_time = self.util.task_waiting_time(counter, current_task.arrival_time)

            if current_task:
                gant_string += current_task.id
                current_task.cpu_burst_needed -= 1
                current_task, finished_tasks = self.process_finished_task(current_task, finished_tasks, counter)

            else:
                gant_string += "-"

            counter += 1  # Increment counter regardless of tasks

        self.printer.gant_printer(gant_string)
        self.printer.turnaround_printer(task_list)
        self.printer.waiting_time_printer(task_list)
        self.revert_cpu_burst(task_list)

    def spf(self, task_list):
        counter = 0
        queue = []
        gant_string: str = ""
        current_task: Task = None
        finished_tasks = []
        task_list: list[Task] = sorted(task_list, key=lambda x: x.arrival_time)
        copy_task_list = task_list[:]

        while len(finished_tasks) != len(task_list):

            # if there are still tasks in task list append it to queue if the first index of the task_list.arrival time == is equal to the counter
            if copy_task_list:
                queue, copy_task_list = self.add_to_queue(copy_task_list, counter, queue)

            # if queue has tasks
            if queue:
                # check our current task
                # sort our queue by cpu burst
                queue = sorted(queue, key=lambda x: x.cpu_burst)

                # check first in q and if we dont have a current task if both are true
                if not current_task:
                    # current task will be the first in q then change task attributes
                    current_task = queue.pop(0)
                    current_task.time_executed.append(counter)
                    current_task.waiting_time = self.util.task_waiting_time(counter, current_task.arrival_time)

            if current_task:
                gant_string += current_task.id
                current_task.cpu_burst_needed -= 1
                current_task, finished_tasks = self.process_finished_task(current_task, finished_tasks, counter)

            else:
                gant_string += "-"

            counter += 1  # Increment counter regardless of tasks

        self.printer.gant_printer(gant_string)
        self.printer.turnaround_printer(task_list)
        self.printer.waiting_time_printer(task_list)
        self.revert_cpu_burst(task_list)

    def srtf(self, task_list):
        counter = 0
        queue = []
        gant_string = ""
        current_task: Task = None
        finished_tasks = []
        task_list = sorted(task_list, key=lambda x: x.arrival_time)
        copy_task_list = task_list[:]

        while len(finished_tasks) != len(task_list) and counter < 50:
            if copy_task_list:
                queue, copy_task_list = self.add_to_queue(copy_task_list, counter, queue)

            if queue:
                queue = sorted(queue, key=lambda x: x.cpu_burst_needed)
                c_shortest: Task = queue[0]

                if not current_task or c_shortest.cpu_burst_needed < current_task.cpu_burst_needed:
                    if current_task:
                        current_task.shift.append(counter)
                        queue.append(current_task)
                    current_task = queue.pop(0)
                    current_task.time_executed.append(counter)
                    if len(current_task.time_executed) > 1:
                        waiting_time_y = current_task.time_executed[-1] - current_task.shift[-1]
                        current_task.waiting_time = current_task.waiting_time + waiting_time_y
                    else:
                        current_task.waiting_time = self.util.task_waiting_time(counter, current_task.arrival_time)

            if current_task:
                gant_string += current_task.id
                current_task.cpu_burst_needed -= 1

                if current_task.cpu_burst_needed <= 0:
                    current_task.shift.append(counter + 1)
                    current_task.turnaround_time = self.util.task_turnaround_time(counter + 1,
                                                                                  current_task.arrival_time)
                    finished_tasks.append(current_task)
                    current_task = None

            else:
                gant_string += "-"

            counter += 1
            print(counter)
            print([task.id for task in copy_task_list])
            print([task.id for task in queue])
            print([task.id for task in finished_tasks])

        self.printer.gant_printer(gant_string)
        self.printer.turnaround_printer(task_list)
        self.printer.waiting_time_printer(task_list)
        self.revert_cpu_burst(task_list)

    def revert_cpu_burst(self, task_list: list[Task]):
        for task in task_list:
            task.cpu_burst_needed = task.cpu_burst

    def add_to_queue(self, task_list, counter, queue):
        added_tasks = []
        while task_list and task_list[0].arrival_time == counter:
            added_tasks.append(task_list.pop(0))
        if added_tasks:
            queue.extend(added_tasks)
        return queue, task_list

    def check_first_in_q(self, queue: list[Task], counter):
        if queue and queue[0].arrival_time <= counter:
            return True
        return False

    def process_finished_task(self, current_task: Task, finished_tasks: list[Task], counter):
        if current_task.cpu_burst_needed == 0:
            current_task.shift.append(counter + 1)
            current_task.turnaround_time = self.util.task_turnaround_time(counter + 1, current_task.arrival_time)
            finished_tasks.append(current_task)
            current_task = None

        return current_task, finished_tasks


if __name__ == '__main__':
    tasks = []
    algo = Algorithm()
    algoU = algo_util()

    num_tasks = int(input("Enter the number of tasks: "))
    for i in range(num_tasks):
        while True:
            id = input(f"Enter task ID for task {i + 1}: ")
            if len(id) != 1:
                print("Task ID must be a single character. Please try again.")
                continue
            elif Task.check_id_exists(id):
                print("Task ID must be unique. Please try again.")
                continue
            break

        arrival_time = int(input(f"Enter arrival time for task {id}: "))
        cpu_burst = int(input(f"Enter CPU burst for task {id}: "))
        task = Task(id, arrival_time, cpu_burst)
        tasks.append(task)

    while True:
        choice = input("Choose algorithm: \n1. FCFS\n2. SPF\n3. SRTF\nEnter choice (1/2/3): ")

        if choice == '1':
            algo.fcfs(tasks)
            break
        elif choice == '2':
            algo.spf(tasks)
            break
        elif choice == '3':
            algo.srtf(tasks)
            break
        else:
            print("Invalid choice. Please try again.")


