<template>
  <div class="flex flex-row space-x-4 m-4 p-4 bg-white rounded-lg border-4 border-gray-900 overflow-x-auto">
    <addTask :click="addTask" class="ml-4 order-last"/>
    <transition-group name="task" tag="div" class="flex flex-row space-x-4">
      <taskComponent 
        v-for="(task) in tasks"  
        :key="task" 
        @task-finished="handleTaskFinished"
        @task-edit="handleEdit"
        @task-deleted="onTaskDeleted">
      </taskComponent>
    </transition-group>
  </div>
  <div class="m-4 p-4 bg-blue-200 h-24 flex flex-row justify-between">
    <div class="w-2/3">
      
    </div>
    <div>
      <button type="button" @click="checkFinished" class="text-white bg-gray-800 hover:bg-gray-600 font-medium rounded-xl text-xl px-10 py-5 transition-colors duration-300 ease">EXECUTE</button>
    </div>
  </div>
</template>

<script>
import taskComponent from './components/taskComponent.vue';
import addTask from './components/addTask.vue';
import { Task, Algorithm } from './cpu.js';

const algo = new Algorithm()
export default {
  name: 'App',
  components: {
    taskComponent,
    addTask
  },
  data() {
    return {
      tasks: [],
      finishedTasks: [],
      finalTask: [],
      counter: 0,
    };
  },
  created() {
    this.initializeTasks();
  },
  methods: {
    initializeTasks() {
      // Initialization logic, if any
    },
    addTask() {
      this.tasks.push(++this.counter);
      console.log(this.tasks)
    },
    onTaskDeleted(){
      this.tasks.pop()
      console.log(this.tasks)
    },
    handleTaskFinished(task) {
      this.finishedTasks.push(task);
      console.log(this.finishedTasks)
    },
    handleEdit(updatedTask){
      let index = this.finishedTasks.findIndex(task => task.id == updatedTask.id)
      this.finishedTasks.splice(index, 1);

    },
    checkFinished() {
      this.finishedTasks.forEach(task => {
        this.createTask(task.id, task.arrivalTime, task.cpuBurst);
      });
      algo.srtf(this.finalTask)
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
