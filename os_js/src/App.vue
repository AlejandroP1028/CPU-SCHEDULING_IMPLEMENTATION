<template>
  <div class="overflow-auto w-screen h-screen bg-gray-50">
    <div class="flex flex-row space-x-4 my-8 mx-32 p-4 bg-white rounded-lg border-4 border-gray-900 overflow-x-auto">
    <addTask :click="addTask" class="ml-4 order-last" />
    <transition-group name="task" tag="div" class="flex flex-row space-x-4">
      <taskComponent 
        v-for="(task, i) in tasks" 
        :key="task" 
        :taskid="i"
        @task-finished="handleTaskFinished"
        @task-edit="handleEdit"
        @task-deleted="onTaskDeleted"
      />
    </transition-group>
  </div>
  <div class="my-8 mx-32 p-4 h-24 flex flex-row justify-end">
    <div>
      <button type="button" @click="checkFinished" class="text-white bg-gray-800 hover:bg-gray-600 font-medium rounded-xl text-xl px-10 py-5 transition-colors duration-300 ease">EXECUTE</button>
    </div>
  </div>
  <div v-if="gantInfo.length > 0" class="flex flex-col h-96 space-y-4 rounded-lg my-8 mx-32 shadow-lg border-4 border-gray-900 p-4">
    <div class="flex h-1/2 justify-center items-center bg-gray-700">
      <div class="h-3/4 w-3/4 bg-blue-200 rounded-full border-2 border-gray-900 flex flex-row divide-x-4 overflow-hidden">
        <chartChild 
          v-for="(i, index) in gantInfo" 
          :key="index"
          :label="i[1]"
          :length="i[0]"
          :color="index % 2 === 0 ? 'bg-gray-200' : 'bg-gray-300'"
          :total = "totalLen"
        />
      </div>
    </div>
    <div class="flex h-1/2 bg-blue-700"></div>
  </div>
  </div>
  
</template>

<script>
import taskComponent from './components/taskComponent.vue';
import addTask from './components/addTask.vue';
import chartChild from './components/chartChild.vue';
import { Task, Algorithm, AlgoUtil } from './cpu.js';

const algo = new Algorithm();
const algoU = new AlgoUtil();

export default {
  name: 'App',
  components: {
    taskComponent,
    addTask,
    chartChild
  },
  data() {
    return {
      tasks: [],
      finishedTasks: [],
      finalTask: [],
      gantInfo: [],
      totalLen: 0,
      info: null,
      counter: 0,
    };
  },
  methods: {
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
      let index = this.finishedTasks.findIndex(task => task.id == updatedTask.id);
      this.finishedTasks.splice(index, 1);
    },
    checkFinished() {
      let num = 0;
      this.finishedTasks.forEach(task => {
        this.createTask(task.id, task.arrivalTime, task.cpuBurst);
      });
      this.info = algo.srtf(this.finalTask);
      algoU.removeTasks();
      this.finalTask = [];

      this.gantInfo = this.info['gantString'].split('|').filter(s => s != '').map(s => [s.length, this.findChar(s)]);
      this.gantInfo.forEach(i => num += i[0]);
      this.totalLen = num;
    },
    findChar(string) {
      return string[0] == '@' ? ' ' : string[Math.floor(string.length / 2)];
    },
    createTask(id, arrivalTime, cpuBurst) {
      let task = new Task(id, arrivalTime, cpuBurst);
      this.finalTask.push(task);
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
  background: rgb(17, 24, 39);
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
</style>
