<template>
    <div class="h-full flex relative items-center justify-center" :style="growStyle" :class="[color,borderClass]">
      <h1 class="text-xl font-bold">{{ capitalizedLabel }}</h1>
      <div class="absolute bottom-0 right-0 translate-x-1/2 translate-y-8 p-1 z-10">
        <h1 class="text-lg font-bold"> {{ length }}</h1>
      </div>
      <div v-if="first" class="absolute bottom-0 left-0 translate-y-8 z-10">
        <h1 class="text-lg font-bold"> 0 </h1>
      </div>
    </div>
  </template>
  
  
  <script>
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
      console.log(`first:${this.first},last:${this.last}`);
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
        return this.first ? 'rounded-l-lg' : this.last ? 'rounded-r-lg' : ''
      }
    }
  };
  </script>
  

  
  <style scoped>
  </style>
  