<template>
    <div class="flex flex-row rounded-full border border-gray-900 w-full">
      <qTask 
        v-for="task in tasks" 
        :key="task.id"
        :task="task" 
      />
    </div>
  </template>
  
  <script>
  import qTask from './qTask.vue';
  
  export default {
    name: 'queuePreview',
    components: {
      qTask
    },
    props: {
      tasks: {
        type: Array,
        required: true
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add any scoped styles if needed */
  </style>
  