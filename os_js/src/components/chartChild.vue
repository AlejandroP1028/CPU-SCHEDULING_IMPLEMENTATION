<template>
    <div class="h-full flex relative items-center justify-center text-gray-900" :style="growStyle" :class="[color,borderClass]">
      <h1 class="text-xl font-bold">{{ capitalizedLabel }}</h1>
      <div class="absolute bottom-0 right-0 translate-x-1/2 translate-y-8 p-1 z-10 text-white">
        <h1 class="text-md font-medium"> {{ shifted }}</h1>
      </div>
      <div v-if="first" class="absolute bottom-0 left-0 translate-y-8 z-10 text-white">
        <h1 class="text-md font-medium"> 0 </h1>
      </div>
    </div>
  </template>
  
  
  <script>
  // use shifted instead of length, placeholder lang talaga yung length jan
  export default {
    name: 'chartChild',
    props: {
      length: Number,
      label: String,
      color: String,
      total: Number,
      shifted: Number,
      first: Boolean,
      last: Boolean
    },
    data() {
      return {
        percentage: 0
      };
    },
    created() {
      this.percentage = ((this.length / this.total) * 100).toFixed(2);
    },
    computed: {
      growStyle() {
        return {
          flexGrow: (this.length / this.total).toFixed(2)
        };
      },
      capitalizedLabel() {
        return this.label.toUpperCase();
      },
      borderClass(){
        return this.first ? 'rounded-l-full' : this.last ? 'rounded-r-full' : ''
      }
    }
  };
  </script>
  

  
  <style scoped>
  </style>
  