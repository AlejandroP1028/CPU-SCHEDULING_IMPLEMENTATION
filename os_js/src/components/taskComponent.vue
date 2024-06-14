<template>
  <div v-if="!deleted" 
       :class="['min-w-64 p-4 rounded-lg shadow-lg bg-gray-800', finished ? 'outline outline-2  outline-emerald-600' : '']">
    <div v-if="!finished">
      <div>
        <div class="flex justify-end">
          <button type="button" @click="deleteDiv">
            <svg class="rounded-full hover:bg-red-600 w-6 h-6 text-white fill-current transition-colors duration-300 ease" xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960" width="24px" fill="currentFill">
              <path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/>
            </svg>
          </button>
        </div>

        <label for="task_id" class="block mb-2 text-sm font-medium text-white">Task ID:</label>
        <input 
          type="text" 
          name="task_id" 
          class="bg-gray-700 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" 
          v-model="id" 
          maxlength="1"
        />
      </div>
      <div>
        <label for="arrival_time" class="block mb-2 text-sm font-medium text-white">Arrival Time:</label>
        <input 
          type="number" 
          min="0"
          name="arrival_time" 
          class="bg-gray-700 text-white text-sm rounded-lg block w-full p-2.5" 
          v-model.number="arrivalTime" 
        />
      </div>
      <div>
        <label for="burst_time" class="block mb-2 text-sm font-medium text-white">Burst Time:</label>
        <input 
          type="number" 
          name="burst_time" 
          min="1"
          class="bg-gray-700 text-white text-sm rounded-lg block w-full p-2.5" 
          v-model.number="cpuBurst" 
        />
      </div>
      <div class="mt-4 flex justify-center">
        <button type="button" @click="checkFinished" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 focus:outline-none">Submit</button>
      </div>
      <div v-if="error" class="text-red-500 mt-2">{{ error }}</div>
    </div>
    <div v-else>
      <div class="mt-6">
        <div class="block mb-2 text-sm font-medium text-white">Task ID:</div>
        <div name="taskId" class="bg-gray-700 text-white text-sm rounded-lg block w-full p-2.5">
          {{ id }} 
        </div>
      </div>
      <div>
        <div class="block mb-2 text-sm font-medium text-white">Arrival Time:</div>
        <div name="arrivalTime" class="bg-gray-700 text-white text-sm rounded-lg block w-full p-2.5">
          {{ arrivalTime }} 
        </div>
      </div>
      <div>
        <div class="block mb-2 text-sm font-medium text-white">Burst Time: </div>
        <div name="cpuBurst" class="bg-gray-700 text-white text-sm rounded-lg block w-full p-2.5">
          {{ cpuBurst }} 
        </div>
      </div>
      <div class="mt-4 flex justify-center">
        <button type="button" @click="edit" class="text-white bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5">Edit</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'taskComponent',
  props: {
    taskid: String
  },
  data() {
    return {
      id: '',
      arrivalTime: 0,
      cpuBurst: 0,
      finished: false,
      deleted: false,
      error: ''
    };
  },
  watch: {
    id(newVal) {
      this.id = newVal.toUpperCase();
    }
  },
  methods: {
    checkFinished() {
      this.finished = this.id && this.arrivalTime >= 0 && this.cpuBurst >= 1;
      if (this.finished) {
        this.$emit('check-duplicate', { id: this.id }, isDuplicate => {
          if (isDuplicate) {
            this.error = 'Duplicate Task ID';
            this.finished = false;
          } else {
            this.error = '';
            this.$emit('task-finished', { id: this.id, arrivalTime: this.arrivalTime, cpuBurst: this.cpuBurst });
          }
        });
      }
    },
    edit() {
      this.finished = !this.finished;
      this.$emit('task-edit', { id: this.id, arrivalTime: this.arrivalTime, cpuBurst: this.cpuBurst });
    },
    deleteDiv() {
      this.$emit('task-deleted', this.taskid);
      this.deleted = !this.deleted;
    }
  },
};
</script>
