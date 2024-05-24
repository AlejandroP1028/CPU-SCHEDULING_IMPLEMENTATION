<template>
    <div class="min-w-64 h-84 bg-gray-600 rounded-lg shadow-lg flex justify-center items-center">
      <svg @click="click" id="add" class="my-28 p-6 w-32 h-32 rounded-lg hover:bg-gray-400 fill-current text-gray-100 hover:text-gray-700 hover:cursor-pointer transition-colors duration-300 ease-in-out" xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960">
        <path d="M440-440H200v-80h240v-240h80v240h240v80H520v240h-80v-240Z"/>
      </svg>
    </div>
  </template>
  
  <script>
  export default {
    name: 'addTask',
    props:{
        click: Function,
    }
  };
  </script>
  