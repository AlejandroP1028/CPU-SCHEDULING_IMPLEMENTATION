<template>
  <div class="flex flex-row space-x-4 m-4 p-4 bg-white rounded-lg border-4 border-gray-900 overflow-x-auto min-w-max">
    <addTask :click="addTask" class="ml-4 order-last"/>
    <taskComponent 
      v-for="(task) in tasks"  
      :key="task" >
    </taskComponent>
  </div>
</template>

<script>
import taskComponent from './components/taskComponent.vue';
import addTask from './components/addTask.vue';

export default {
  name: 'App',
  components: {
    taskComponent,
    addTask
  },
  data() {
    return {
      tasks: [],
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
    addTask(){
      this.tasks.push(++this.counter);
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
</style>
