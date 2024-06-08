<template>
  <div class="overflow-auto w-screen h-screen bg-gray-50 dark:bg-gray-900">
    <div class="flex flex-row my-8 mx-64">
      <h1 v-if="taskTitle" class="text-xl text-white font-bold">Algorithm Chosen: {{ taskTitle }}</h1>

      <div class="ml-auto flex flex-row items-center">
        <div v-if="taskTitle === 'Round Robin'" class="flex flex-row mr-4 items-center">
          <label for="quantum" class="text-white">Time Slice:</label>
          <input 
            type="number" 
            id="quantum" 
            v-model.number="timeQuantum" 
            class="ml-2 p-1 rounded w-12 bg-gray-600 text-white"
            min="1"
          />
        </div>
        <dropdown
          buttonText="Algorithms"
          menuWidth="w-48" 
          :menuItems="menuItems" 
          :divider="true"
          @list-item-click="handleListItemClick"
        />
      </div>
    </div>
    
    <!-- Number input for time quantum of Round Robin, only show if the taskTitle is 'Round Robin' -->

    <div :class="taskTitle ? '' : 'pointer-events-none opacity-50'" class="flex flex-row space-x-4 my-8 mx-64 p-4 bg-gray-700 rounded-lg overflow-x-auto">
      <addTask :click="addTask" class="ml-4 order-last" />
      <transition-group name="task" tag="div" class="flex flex-row space-x-4">
        <taskComponent 
          v-for="(task, i) in tasks" 
          :key="task" 
          :taskid="i"
          @task-finished="handleTaskFinished"
          @task-edit="handleEdit"
          @task-deleted="onTaskDeleted"
          @check-duplicate="checkDuplicate"
        />
      </transition-group>
    </div>

    <div class="my-8 mx-64 p-4 h-24 flex flex-row justify-end">
      <div>
        <button type="button" @click="checkFinished" class="text-white bg-gray-600 hover:bg-gray-600 font-medium rounded-xl text-xl px-10 py-5 transition-colors duration-300 ease">EXECUTE</button>
      </div>
    </div>
    
    <div v-if="gantInfo.length > 0" class="flex flex-col h-[500px] space-y-4 my-8 mx-64 rounded-md bg-gray-700 shadow-lg p-4">
      <div class="flex h-1/2 flex-col justify-center text-white items-center">
        <h1 class="text-3xl font-bold mb-4">{{taskTitle}}</h1>
        <h1 class="text-3xl font-bold mb-8">Gantt Chart</h1>
        <div class="h-1/2 w-3/4 flex flex-row divide-x-4">
          <chartChild 
            v-for="(i, index) in gantInfo" 
            :key="index"
            :label="i[1]"
            :length="i[0]"
            :shifted="shifted[index]"
            :color="index % 2 === 0 ? 'bg-gray-200' : 'bg-gray-300'"
            :total="totalLen"
            :first="index === 0 ? true : false"
            :last="index === gantInfo.length - 1 ? true : false"
          />
        </div>
      </div>
      <div class="flex h-1/2 "></div>
    </div>
  </div>
</template>

<script>
import taskComponent from './components/taskComponent.vue';
import addTask from './components/addTask.vue';
import chartChild from './components/chartChild.vue';
import dropdown from './components/dropdown.vue';
import { Task, Algorithm, AlgoUtil } from './cpu.js';

const algo = new Algorithm();
const algoU = new AlgoUtil();

export default {
  name: 'App',
  components: {
    taskComponent,
    addTask,
    chartChild,
    dropdown
  },
  data() {
    return {
      taskTitle: null,
      shifted: null,
      tasks: [],
      finishedTasks: [],
      finalTask: [],
      gantInfo: [],
      totalLen: 0,
      info: null,
      counter: 0,
      timeQuantum: 3,  // Default value for Round Robin time quantum
      menuItems: [
        { label: 'First Come First Serve', type: 'default' },
        { label: 'Shortest Process First', type: 'default' },
        { label: 'Shortest Remaining Time First', type: 'default' },
        { label: 'Round Robin', type: 'default' },
      ]
    };
  },
  methods: {
    handleListItemClick(item) {
      this.taskTitle = item.label;
      this.gantInfo = [];
    },
    addTask() {
      this.tasks.push(++this.counter);
    },
    onTaskDeleted(index) {
      this.tasks.splice(index, 1);
    },
    handleTaskFinished(task) {
      this.finishedTasks.push(task);
    },
    handleEdit(updatedTask) {
      let index = this.finishedTasks.findIndex(task => task.id === updatedTask.id);
      this.finishedTasks.splice(index, 1);
    },
    checkFinished() {
      if (!this.taskTitle) return;
      
      let num = 0;
      this.finishedTasks.forEach(task => {
        this.createTask(task.id, task.arrivalTime, task.cpuBurst);
      });

      // Execute the selected algorithm
      switch (this.taskTitle) {
        case 'First Come First Serve':
          this.info = algo.fcfs(this.finalTask);
          break;
        case 'Shortest Process First':
          this.info = algo.spf(this.finalTask);
          break;
        case 'Shortest Remaining Time First':
          this.info = algo.srtf(this.finalTask);
          break;
        case 'Round Robin':
          this.info = algo.rr(this.finalTask, this.timeQuantum); // Use the timeQuantum for Round Robin
          break;
        default:
          console.error('Unknown algorithm:', this.taskTitle);
          return;
      }

      algoU.removeTasks();
      this.finalTask = [];

      this.gantInfo = this.info['gantString'].split('|').filter(s => s !== '').map(s => [s.length, this.findChar(s)]);

      let rtaskList = this.info['taskList'];
      let combinedShifted = new Set([]);

      for (let task of rtaskList) {
        for (let shift of task.shift) {
          combinedShifted.add(shift);
        }
        for (let start of task.timeExecuted) {
          combinedShifted.add(start);
        }
      }

      combinedShifted = new Set([...combinedShifted].sort((a, b) => a - b));
      
      if (combinedShifted.has(0)) {
        combinedShifted.delete(0);
      }
      this.shifted = [...combinedShifted];

      this.gantInfo.forEach(i => num += i[0]);
      this.totalLen = num;
    },
    findChar(string) {
      return string[0] === '@' ? ' ' : string[Math.floor(string.length / 2)];
    },
    createTask(id, arrivalTime, cpuBurst) {
      let task = new Task(id, arrivalTime, cpuBurst);
      this.finalTask.push(task);
    },
    checkDuplicate(task, callback) {
      const isDuplicate = this.finishedTasks.some(t => t.id === task.id);
      callback(isDuplicate);
    }
  }
};
</script>

<style scoped>
/* Custom scrollbar for the horizontal task container */
::-webkit-scrollbar {
  height: 4px;
}
::-webkit-scrollbar-thumb {
  background: white;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgb(55, 66, 99);
}

/* Add animations */
.task-enter-active, .task-leave-active {
  transition: all 0.5s ease;
}
.task-enter, .task-leave-to /* .task-leave-active in <2.1.8 */ {
  transform: translateX(-10%);
  opacity: 0;
}

/* Disable interaction and make semi-transparent when no algorithm is selected */
.pointer-events-none {
  pointer-events: none;
  opacity: 0.5;
}
</style>
