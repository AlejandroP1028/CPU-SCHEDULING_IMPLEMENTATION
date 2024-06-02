<template>
  <div class="overflow-auto w-screen h-screen bg-gray-50">
    <div class="flex flex-row space-x-4 my-8 mx-64 p-4 bg-white rounded-lg border-4 border-gray-900 overflow-x-auto">
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
  <div class="my-8 mx-64 p-4 h-24 flex flex-row justify-end">
    <div>
      <button type="button" @click="checkFinished" class="text-white bg-gray-800 hover:bg-gray-600 font-medium rounded-xl text-xl px-10 py-5 transition-colors duration-300 ease">EXECUTE</button>
    </div>
  </div>
  <div v-if="gantInfo.length > 0" class="flex flex-col h-[500px] space-y-4 my-8 mx-64 rounded-md  shadow-lg border-4 border-gray-900 p-4">
    
    <div class="flex h-1/2 flex-col justify-center items-center">
      <h1 class="text-3xl font-bold mb-4">{{algo}}</h1>
      <h1 class="text-3xl font-bold mb-8">Gantt Chart</h1>

      <div class="h-1/2 w-3/4 flex flex-row divide-x-4 border rounded-full border-gray-900">
        <chartChild 
          v-for="(i, index) in gantInfo" 
          :key="index"
          :label="i[1]"
          :length="i[0]"
          :color="index % 2 === 0 ? 'bg-gray-200' : 'bg-gray-300'"
          :total = "totalLen"
          :first = "index === 0 ? true : false"
          :last = "index === (gantInfo.length - 1) ? true : false"
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
      algo: 'SRTF',
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
      //remote tasks inside for next iteration
      algoU.removeTasks();
      this.finalTask = [];


      //get the gantinfo from info object received from algo class returns an array of array [length,char] 
      this.gantInfo = this.info['gantString'].split('|').filter(s => s != '').map(s => [s.length, this.findChar(s)]);

      //pwede mong gawin either or 

      //first:find the shifted value of sorted task from this.info['taskList']...
      //pwede mo siyang gawan ng value pair or array of array with the id tas taskshifted tapos gawa ka bagong data attribute tas don mo istore
      //then somehow ipapasa mo siya sa chartchild or some shit
      console.log("tasklist",this.info['taskList'])

      //second:display the waiting time and turnaround time from this.info['ta'] and this.info['wt']
      console.log("ta",this.info['ta'])
      console.log("wt",this.info['wt'])

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
