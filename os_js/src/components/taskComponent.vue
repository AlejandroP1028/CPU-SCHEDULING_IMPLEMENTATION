<template>
  <div v-if="!deleted" class="min-w-64 p-4 bg-gray-200 rounded-lg shadow-lg">
    <div v-if="!finished">
      <div>
        <div class="flex justify-end">
          <button type="button" @click="deleteDiv">
            <svg class="rounded-full hover:bg-gray-200" xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="currentFill"><path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/></svg>
          </button>
        </div>

          <label for="task_id" class="block mb-2 text-sm font-medium text-gray-900">Task ID:</label>
        <input 
          type="text" 
          name="task_id" 
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" 
          v-model="id" 
        />
      </div>
      <div>
        <label for="arrival_time" class="block mb-2 text-sm font-medium text-gray-900">Arrival Time:</label>
        <input 
          type="number" 
          name="arrival_time" 
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" 
          v-model.number="arrivalTime" 
        />
      </div>
      <div>
        <label for="burst_time" class="block mb-2 text-sm font-medium text-gray-900">Burst Time:</label>
        <input 
          type="number" 
          name="burst_time" 
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" 
          v-model.number="cpuBurst" 
        />
      </div>
      <div class="mt-4 flex justify-center">
        <button type="button" @click="checkFinished" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 focus:outline-none ">Submit</button>
      </div>
      
    </div>
    <div v-else>
      <div class="mt-6">
          <div class="block mb-2 text-sm font-medium text-gray-900">Task ID:</div>
        <div
          name="taskId" 
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" >
          {{this.id}} 
        </div>

      </div>
      <div>
        <div class="block mb-2 text-sm font-medium text-gray-900">Arrival Time:</div>
        <div
          name="arrivalTime" 
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" >
          {{this.arrivalTime}} 
        </div>
      </div>
      <div>
        <div class="block mb-2 text-sm font-medium text-gray-900">Burst Time: </div>
        <div
          name="cpuBurst" 
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" >
          {{this.cpuBurst}} 
        </div>
      </div>
      <div class="mt-4 flex justify-center">
        <button type="button" @click="edit" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 focus:outline-none ">Edit</button>
      </div>
      
    </div>
  </div>
</template>

<script>
export default {
  name: 'taskComponent',
  props: {
  },
  data() {
    return {
      finished: false,
      deleted: false
    };
  },
  methods: {
    checkFinished() {
      this.finished = this.id && this.arrivalTime && this.cpuBurst ;
    },
    edit() {
      this.finished = !this.finished;
    },
    deleteDiv(){
      this.deleted = !this.deleted
    }
  },
  watch: {
    id: 'checkFinished',
    arrivalTime: 'checkFinished',
    cpuBurst: 'checkFinished'
  },
};
</script>

<style scoped>
/* Add any scoped styles if needed */
</style>
