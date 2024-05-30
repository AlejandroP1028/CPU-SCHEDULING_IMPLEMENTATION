<template>
    <div class="h-full flex items-center justify-center" :style="growStyle" :class="color">
      <h1 class="text-xl font-bold">{{ capitalizedLabel }}</h1>
    </div>
  </template>
  
  
  <script>
  export default {
    name: 'chartChild',
    props: {
      length: Number,
      label: String,
      color: String,
      total: Number
    },
    data() {
      return {
        percentage: 0
      };
    },
    created() {
      this.percentage = ((this.length / this.total) * 100).toFixed(2);
      console.log(this.percentage);
    },
    computed: {
      growStyle() {
        return {
          flexGrow: (this.length / this.total).toFixed(2)
        };
      },
      capitalizedLabel() {
        return this.label.toUpperCase();
      }
    }
  };
  </script>
  

  
  <style scoped>
  </style>
  