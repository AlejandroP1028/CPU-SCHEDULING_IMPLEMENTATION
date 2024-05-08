from task import Task
from algoUtil import algoUtil
from algorithm import Algorithm

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
