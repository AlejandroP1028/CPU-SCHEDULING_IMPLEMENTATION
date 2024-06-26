let task = [];

class Task {
  constructor(id, arrivalTime, cpuBurst) {
    if (id.length !== 1) {
      throw new Error("Task ID must be a single character.");
    }
    if (this.checkId(id)) {
      throw new Error("Task ID must be unique.");
    }
    this.id = id;
    this.arrivalTime = arrivalTime;
    this.cpuBurst = cpuBurst;
    this.cpuBurstNeeded = cpuBurst;
    this.waitingTime = 0;
    this.turnaroundTime = 0;
    this.timeExecuted = []; // Time when executed can be 1 or many depending on the process
    this.shift = []; // Time shifted value can be 1 or more depending on the process
    task.push(this);
  }

  checkId(id) {
    return task.some((task) => task.id === id);
  }

  toString() {
    return `ID: ${this.id}
  Arrival Time: ${this.arrivalTime}
  CPU Burst: ${this.cpuBurst}
  CPU Burst Needed: ${this.cpuBurstNeeded}
  Waiting Time: ${this.waitingTime}
  Turnaround Time: ${this.turnaroundTime}
  Time Executed: ${this.timeExecuted}
  Time Shifted: ${this.shift}`;
  }


}

class AlgoUtil {
  getTotalBurst(taskList) {
    let totalBurst = 0;
    for (let task of taskList) {
      totalBurst += task.cpuBurst;
    }
    return totalBurst;
  }
  
  taskWaitingTime(timeExecuted, arrivalTime) {
    // waiting time = time executed - arrival time
    return timeExecuted - arrivalTime;
  }

  taskTurnaroundTime(timeOfCompletion, arrivalTime) {
    // time of completion - arrival time
    return timeOfCompletion - arrivalTime;
  }

  avg(lst) {
    let num = 0;
    for (let i of lst) {
      num += i;
    }
    return num / lst.length;
  }

  removeTasks() {
    task = [];
  }
}

class AlgoPrinter {
  constructor() {
    this.util = new AlgoUtil();
  }
  // aaabbbbcccc--ddddd
  
  gantPrinter(gantString) {
    let finalString = "";
    let strList = [...gantString];
    let currentChar = null;
    let currentCharCount = 0;

    //aaaaabbaaaa
    //--a--|-b|--a-|@@
    //finalstring = |--a--
    //currentchar = b
    //charcount = 5
    // if 3 then char
    for (let char of strList) {
      if (currentChar === char) {
        currentCharCount += 1;
      } 
      else {
        if (currentChar) {
          finalString += "|";
          for (let x = 0; x < currentCharCount; x++) {
            if (x === Math.floor(currentCharCount / 2)) {
              if (currentChar === "-") {
                finalString += "@";
              } else {
                finalString += currentChar;
              }
            } else {
              if (currentChar === "-") {
                finalString += "@";
              } else {
                finalString += "-";
              }
            }
          }
          currentCharCount = 0; // Reset count for the new character
        }
        currentChar = char;
        currentCharCount = 1;
      }
    }

    // Append the remaining characters after the loop ends
    if (currentChar) {
      finalString += "|";
      for (let x = 0; x < currentCharCount; x++) {
        if (x === Math.floor(currentCharCount / 2)) {
          finalString += currentChar;
        } else {
          if (currentChar === "-") {
            finalString += " ";
          } else {
            finalString += "-";
          }
        }
      }
    }
    finalString += "|";
    return finalString;
  }

  turnaroundPrinter(taskList) {
    let turnaroundList = [];
    let turnaroundStr = "Turnaround Time:\n";
    for (let task of taskList) {
      turnaroundList.push(task.turnaroundTime);
      turnaroundStr += `TA ${task.id.toLowerCase()} = ${task.turnaroundTime}ms\n`;
    }

    turnaroundStr += `Average TA: ${this.util.avg(turnaroundList)}ms`;
    return turnaroundStr;
  }

  waitingTimePrinter(taskList) {
    console.log(taskList)
    let waitingTime = [];
    let waitingTimeStr = "Waiting Time:\n";
    for (let task of taskList) {
      waitingTime.push(task.waitingTime);
      waitingTimeStr += `WT ${task.id.toLowerCase()} = ${task.waitingTime}ms\n`;
    }

    waitingTimeStr += `Average WT: ${this.util.avg(waitingTime)}ms`;
    return waitingTimeStr;
  }
}

class Algorithm {
  constructor() {
    this.printer = new AlgoPrinter();
    this.util = new AlgoUtil();
  }

  fcfs(taskList) {
    let counter = 0;
    let queue = [];
    let gantString = "";
    let currentTask = null;
    let finishedTasks = [];
    taskList.sort((a, b) => a.arrivalTime - b.arrivalTime);
    let copyTaskList = [...taskList];

    while (finishedTasks.length !== taskList.length) {
      if (copyTaskList.length > 0) {
        [queue, copyTaskList] = this.addToQueue(copyTaskList, counter, queue);
      }
      if (queue.length > 0) {
        if (this.checkFirstInQueue(queue, counter) && !currentTask) {
          currentTask = queue.shift();
          currentTask.timeExecuted.push(counter);
          currentTask.waitingTime = this.util.taskWaitingTime(counter, currentTask.arrivalTime);
        }
      }

      if (currentTask) {
        gantString += currentTask.id;
        currentTask.cpuBurstNeeded -= 1;
        [currentTask, finishedTasks] = this.processFinishedTask(currentTask, finishedTasks, counter);
      } else {
        gantString += "-";
      }

      counter += 1; // Increment counter regardless of tasks
    }


    let gs = this.printer.gantPrinter(gantString);
    let ta = this.printer.turnaroundPrinter(taskList);
    let wt = this.printer.waitingTimePrinter(taskList);
    let tl = finishedTasks;

    counter = 0;
    this.revertCpuBurst(taskList);

    return {
      gantString: gs,
      ta: ta,
      wt: wt,
      taskList: tl,
    };
  }

  spf(taskList) {
    let counter = 0;
    let queue = [];
    let gantString = "";
    let currentTask = null;
    let finishedTasks = [];
    let copyTaskList = [...taskList].sort((a, b) => a.arrivalTime - b.arrivalTime);

    while (finishedTasks.length !== taskList.length) {
      if (copyTaskList.length > 0) {
        [queue, copyTaskList] = this.addToQueue(copyTaskList, counter, queue);
      }

      if (queue.length > 0) {
        queue.sort((a, b) => a.cpuBurst - b.cpuBurst);

        if (!currentTask) {
          currentTask = queue.shift();
          currentTask.timeExecuted.push(counter);
          currentTask.waitingTime = this.util.taskWaitingTime(counter, currentTask.arrivalTime);
        }
      }

      if (currentTask) {
        gantString += currentTask.id;
        currentTask.cpuBurstNeeded -= 1;
        [currentTask, finishedTasks] = this.processFinishedTask(currentTask, finishedTasks, counter);
      } else {
        gantString += "-";
      }

      counter += 1; // Increment counter regardless of tasks
    }

    let gs = this.printer.gantPrinter(gantString);
    let ta = this.printer.turnaroundPrinter(taskList);
    let wt = this.printer.waitingTimePrinter(taskList);
    let tl = finishedTasks;

    counter = 0;
    this.revertCpuBurst(taskList);

    return {
      gantString: gs,
      ta: ta,
      wt: wt,
      taskList: tl,
    };
  }


  srtf(taskList) {
    let counter = 0;
    let queue = [];
    let gantString = "";
    let currentTask = null;
    let finishedTasks = [];
    let copyTaskList = [...taskList].sort((a, b) => a.arrivalTime - b.arrivalTime);

    while (finishedTasks.length !== taskList.length) {
      if (copyTaskList.length > 0) {
        [queue, copyTaskList] = this.addToQueue(copyTaskList, counter, queue);
      }

      if (queue.length > 0) {
        queue.sort((a, b) => a.cpuBurstNeeded - b.cpuBurstNeeded);
        let shortestTask = queue[0];

        if (!currentTask || shortestTask.cpuBurstNeeded < currentTask.cpuBurstNeeded) {
          if (currentTask) {
            currentTask.shift.push(counter);
            queue.push(currentTask);
          }
          currentTask = queue.shift();
          currentTask.timeExecuted.push(counter);
          if (currentTask.timeExecuted.length > 1) {
            let waitingTimeY = currentTask.timeExecuted[currentTask.timeExecuted.length - 1] - currentTask.shift[currentTask.shift.length - 1];
            currentTask.waitingTime += waitingTimeY;
          } else {
            currentTask.waitingTime = this.util.taskWaitingTime(counter, currentTask.arrivalTime);
          }
        }
      }

      if (currentTask) {
        gantString += currentTask.id;
        currentTask.cpuBurstNeeded -= 1;

        if (currentTask.cpuBurstNeeded <= 0) {
          currentTask.shift.push(counter + 1);
          currentTask.turnaroundTime = this.util.taskTurnaroundTime(counter + 1, currentTask.arrivalTime);
          gantString += '|';
          finishedTasks.push(currentTask);
          currentTask.shift.push(counter + 1);
          currentTask = null;
        }
      } else {
        gantString += "-";
      }

      counter += 1;
    }

    let gs = this.printer.gantPrinter(gantString);
    let ta = this.printer.turnaroundPrinter(taskList);
    let wt = this.printer.waitingTimePrinter(taskList);
    let tl = finishedTasks;

    counter = 0;
    this.revertCpuBurst(taskList);

    return {
      gantString: gs,
      ta: ta,
      wt: wt,
      taskList: tl,
    };
  }

  rr(taskList, timeSlice) {
    let bol = false
    let counter = 0;
    let currentSlice = timeSlice;
    let queue = [];
    let gantString = "";
    let currentTask = null;
    let finishedTasks = [];
    taskList.sort((a, b) => a.arrivalTime - b.arrivalTime);
    let copyTaskList = [...taskList];

    while (finishedTasks.length !== taskList.length) {
      // Add new tasks to the queue as they arrive
      if (copyTaskList.length > 0) {
        [queue, copyTaskList] = this.addToQueue(copyTaskList, counter, queue);
      }

      // If no current task and queue is not empty, get the next task
      if (!currentTask && queue.length > 0) {
        currentTask = queue.shift();
        currentTask.timeExecuted.push(counter);
        if (currentTask.timeExecuted.length === 1) {
          currentTask.waitingTime = this.util.taskWaitingTime(counter, currentTask.arrivalTime);
        } else {
          let waitingTimeY = currentTask.timeExecuted[currentTask.timeExecuted.length - 1] - currentTask.shift[currentTask.shift.length - 1];
          currentTask.waitingTime += waitingTimeY;
        }
        currentSlice = timeSlice;
      }

      // Process the current task if it exists
      if (currentTask) {
        gantString += currentTask.id;
        currentTask.cpuBurstNeeded -= 1;
        currentSlice -= 1;

        // If current task finishes, calculate turnaround time and remove it
        if (currentTask.cpuBurstNeeded === 0) {
          currentTask.turnaroundTime = this.util.taskTurnaroundTime(counter + 1, currentTask.arrivalTime);
          gantString += '|'
          currentTask.shift.push(counter + 1);
          finishedTasks.push(currentTask);
          currentTask = null;
          currentSlice = timeSlice;
        } else if (currentSlice === 0) {
          // If time slice is over, put task back in queue and reset slice
          bol = true
          gantString += '|'
          counter += 1
          currentTask.shift.push(counter);
          [queue, copyTaskList] = this.addToQueue(copyTaskList, counter, queue);
          queue.push(currentTask);
          currentTask = null;
          currentSlice = timeSlice;
        }
      } else {
        gantString += "-";
      }

      // Update waiting time for all tasks in the queue
      if (!bol) {

        counter += 1;
      }

      bol = false
      // Increment counter regardless of tasks
    }

    let gs = this.printer.gantPrinter(gantString);
    let ta = this.printer.turnaroundPrinter(taskList);
    let wt = this.printer.waitingTimePrinter(taskList);
    let tl = finishedTasks;

    counter = 0;
    this.revertCpuBurst(taskList);

    return {
      gantString: gs,
      gs: gantString,
      ta: ta,
      wt: wt,
      taskList: tl,
    };
  }



  revertCpuBurst(taskList) {
    for (let task of taskList) {
      task.cpuBurstNeeded = task.cpuBurst;
    }
  }

  addToQueue(taskList, counter, queue) {
    while (taskList.length > 0 && taskList[0].arrivalTime <= counter) {
      queue.push(taskList.shift());
    }
    return [queue, taskList];
  }


  checkFirstInQueue(queue, counter) {
    if (queue.length > 0 && queue[0].arrivalTime <= counter) {
      return true;
    }
    return false;
  }

  processFinishedTask(currentTask, finishedTasks, counter) {
    if (currentTask.cpuBurstNeeded === 0) {
      currentTask.shift.push(counter + 1);
      currentTask.turnaroundTime = this.util.taskTurnaroundTime(counter + 1, currentTask.arrivalTime);
      finishedTasks.push(currentTask);
      currentTask = null;
    }
    return [currentTask, finishedTasks];
  }
}


module.exports = {
  Task,
  AlgoUtil,
  AlgoPrinter,
  Algorithm,
};
