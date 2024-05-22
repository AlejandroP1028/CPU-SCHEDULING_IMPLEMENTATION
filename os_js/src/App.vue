/* eslint-disable */


<template>
  <div>

  </div>
</template>

<script>


import { Task,Algorithm } from './cpu.js';

let tasks = [];
let algo = new Algorithm();

let task1 = new Task('A', 5, 3)
let task2 = new Task('B', 0, 10)
let task3 = new Task('C', 1, 3)
let task4 = new Task('D', 6, 4)
let task5 = new Task('E', 3, 7)

tasks.push(task1, task2, task3, task4, task5)

console.log(tasks)
algo.srtf(tasks)



let f = new Task('A',0,5)

console.log(f)






export default {
  name: 'App',
  components: {
  }
}
</script>

