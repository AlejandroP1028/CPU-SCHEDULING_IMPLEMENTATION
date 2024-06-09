<template>
  <div class="overflow-auto w-screen h-screen bg-gray-900">
    <div class="flex flex-row my-8 mx-64">
      <h1
        v-if="taskTitle"
        class="text-xl text-white font-bold"
        style="font-family: 'Gabarito', sans-serif"
      >
        Algorithm Chosen: {{ taskTitle }}
      </h1>

      <div class="ml-auto flex flex-row items-center">
        <div
          v-if="taskTitle === 'Round Robin'"
          class="flex flex-row mr-4 items-center"
        >
          <label
            for="quantum"
            class="text-white"
            style="font-family: 'Gabarito', sans-serif"
            >Time Slice:</label
          >
          <input
            type="number"
            id="quantum"
            v-model.number="timeQuantum"
            class="ml-2 p-1 rounded w-12 bg-gray-600 text-white"
            min="1"
          />
        </div>
        <dropdown
          buttonText="Choose an Algorithm"
          menuWidth="w-48"
          :menuItems="menuItems"
          @list-item-click="handleListItemClick"
        />
      </div>
    </div>

    <!-- Number input for time quantum of Round Robin, only show if the taskTitle is 'Round Robin' -->

    <div
      :class="taskTitle ? '' : 'pointer-events-none opacity-50'"
      class="flex flex-row space-x-4 my-8 mx-64 p-4 bg-gray-700 rounded-lg overflow-x-auto"
    >
      <addTask :click="addTask" class="ml-4 order-last" />
      <transition-group name="task" tag="div" class="flex flex-row space-x-4">
        <taskComponent
          v-for="(task, i) in tasks"
          :key="task"
          :taskid="i"
          @task-finished="handleTaskFinished"
          @task-edit="handleEdit"
          @task-deleted="onTaskDeleted"
          @check-duplicate="checkDuplicate"
        />
      </transition-group>
    </div>

    <div class="my-8 mx-64 p-4 h-24 flex flex-row justify-end">
      <div>
        <button
          type="button"
          @click="checkFinished"
          class="text-white bg-gray-800 hover:bg-gray-600 font-bold rounded-3xl text-xl px-12 py-3 transition-colors duration-300 ease pulse"
          style="
            filter: drop-shadow(0px 1px 4px rgba(255, 255, 255, 0.8));
            font-family: 'Gabarito', sans-serif;
          "
        >
          Execute
        </button>
      </div>
    </div>

    <div
      v-if="gantInfo.length > 0"
      class="flex flex-col h-[300px] space-y-4 my-8 mx-64 mt-8 rounded-lg bg-gray-700 shadow-lg p-4"
    >
      <div class="flex h-full flex-col text-white items-center">
        <h1
          class="text-3xl font-bold mt-6"
          style="font-family: 'Gabarito', sans-serif"
        >
          {{ taskTitle }}
        </h1>
        <h1
          class="text-3xl font-bold mb-12"
          style="font-family: 'Gabarito', sans-serif"
        >
          Gantt Chart
        </h1>
        <div class="h-2/6 w-3/4 flex flex-row justify-self-center divide-x-4">
          <chartChild
            v-for="(i, index) in gantInfo"
            :key="index"
            :label="i[1]"
            :length="i[0]"
            :shifted="shifted[index]"
            :color="index % 2 === 0 ? 'bg-gray-200' : 'bg-gray-300'"
            :total="totalLen"
            :first="index === 0 ? true : false"
            :last="index === gantInfo.length - 1 ? true : false"
          />
        </div>
      </div>
    </div>

    <div
      v-if="info && info.taskList"
      class="flex flex-col my-8 mx-64 rounded-md bg-gray-700 shadow-lg p-4 text-white"
    >
      <h2
        class="text-2xl font-bold mb-4 self-center"
        style="font-family: 'Gabarito', sans-serif"
      >
        Task Information
      </h2>
      <table class="table-auto w-full text-left">
        <thead>
          <tr>
            <th class="px-4 py-2">Task ID</th>
            <th class="px-4 py-2">Arrival Time</th>
            <th class="px-4 py-2">Burst Time</th>
            <th class="px-4 py-2">Waiting Time</th>
            <th class="px-4 py-2">Turnaround Time</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in info.taskList" :key="task.id">
            <td class="border px-4 py-2">{{ task.id }}</td>
            <td class="border px-4 py-2">{{ task.arrivalTime }}</td>
            <td class="border px-4 py-2">{{ task.cpuBurst }}</td>
            <td class="border px-4 py-2">{{ task.waitingTime }} m/s</td>
            <td class="border px-4 py-2">{{ task.turnaroundTime }} m/s</td>
          </tr>
        </tbody>

        <tfoot>
          <tr>
            <td colspan="3"></td>
            <td class="border px-4 py-2">
              {{ averageWaitingTime.toFixed(2) }} m/s
            </td>
            <td class="border px-4 py-2">
              {{ averageTurnaroundTime.toFixed(2) }} m/s
            </td>
          </tr>
        </tfoot>
      </table>
    </div>

    <div class="absolute right-7 bottom-7">
      <div class="sticky">
        <informationPopover
          position="top"
          popoverColor="slate"
          informationIconColor="slate"
          popoverTitle="Navigating The Website: A Quick Guide"
          popoverContent="Select from the 4 algorithms available, then add a task. </br> Define the task's Task ID, Arrival Time, and Burst Time before hitting execute."
        ></informationPopover>
      </div>
    </div>
  </div>
</template>

<script>
import taskComponent from "./components/taskComponent.vue";
import addTask from "./components/addTask.vue";
import chartChild from "./components/chartChild.vue";
import dropdown from "./components/dropdown.vue";
import { Task, Algorithm, AlgoUtil } from "./cpu.js";
import informationPopover from "./components/informationPopover.vue";

const algo = new Algorithm();
const algoU = new AlgoUtil();

export default {
  name: "App",
  components: {
    taskComponent,
    addTask,
    chartChild,
    dropdown,
    informationPopover,
  },
  data() {
    return {
      taskTitle: null,
      shifted: null,
      tasks: [],
      finishedTasks: [],
      finalTask: [],
      gantInfo: [],
      totalLen: 0,
      info: null,
      counter: 0,
      timeQuantum: 3, // Default value for Round Robin time quantum
      menuItems: [
        { label: "First Come First Serve", type: "default" },
        { label: "Shortest Process First", type: "default" },
        { label: "Shortest Remaining Time First", type: "default" },
        { label: "Round Robin", type: "default" },
      ],
      averageWaitingTime: 0,
      averageTurnaroundTime: 0,
    };
  },
  methods: {
    handleListItemClick(item) {
      this.taskTitle = item.label;
      this.gantInfo = [];
      this.info = null;
    },
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
      let index = this.finishedTasks.findIndex(
        (task) => task.id === updatedTask.id
      );
      this.finishedTasks.splice(index, 1);
    },
    checkFinished() {
      if (!this.taskTitle) return;

      this.finishedTasks.forEach((task) => {
        this.createTask(task.id, task.arrivalTime, task.cpuBurst);
      });

      // Execute the selected algorithm
      switch (this.taskTitle) {
        case "First Come First Serve":
          this.info = algo.fcfs(this.finalTask);
          break;
        case "Shortest Process First":
          this.info = algo.spf(this.finalTask);
          break;
        case "Shortest Remaining Time First":
          this.info = algo.srtf(this.finalTask);
          break;
        case "Round Robin":
          this.info = algo.rr(this.finalTask, this.timeQuantum); // Use the timeQuantum for Round Robin
          break;
        default:
          console.error("Unknown algorithm:", this.taskTitle);
          return;
      }

      algoU.removeTasks();
      this.finalTask = [];

      this.gantInfo = this.info["gantString"]
        .split("|")
        .filter((s) => s !== "")
        .map((s) => [s.length, this.findChar(s)]);
      let waitingTimes = this.info.taskList.map((task) => task.waitingTime);
      let turnaroundTimes = this.info.taskList.map(
        (task) => task.turnaroundTime
      );
      this.averageWaitingTime = algoU.avg(waitingTimes);
      this.averageTurnaroundTime = algoU.avg(turnaroundTimes);

      let rtaskList = this.info["taskList"];
      let combinedShifted = new Set([]);

      for (let task of rtaskList) {
        for (let shift of task.shift) {
          combinedShifted.add(shift);
        }
        for (let start of task.timeExecuted) {
          combinedShifted.add(start);
        }
      }

      combinedShifted = new Set([...combinedShifted].sort((a, b) => a - b));

      if (combinedShifted.has(0)) {
        combinedShifted.delete(0);
      }
      this.shifted = [...combinedShifted];

      let num = this.gantInfo.reduce(
        (accumulator, currentValue) => accumulator + currentValue[0],
        0
      );
      this.totalLen = num;
    },
    findChar(string) {
      return string[0] === "@" ? " " : string[Math.floor(string.length / 2)];
    },
    createTask(id, arrivalTime, cpuBurst) {
      let task = new Task(id, arrivalTime, cpuBurst);
      this.finalTask.push(task);
    },
    checkDuplicate(task, callback) {
      const isDuplicate = this.finishedTasks.some((t) => t.id === task.id);
      callback(isDuplicate);
    },
  },
};
</script>

<style scoped>
@keyframes pulse {
  0% {
    transform: scale(0.97);
  }
  50% {
    transform: scale(1);
  }
  100% {
    transform: scale(0.97);
  }
}

.pulse {
  animation: pulse 1.5s infinite;
}
@import url("https://fonts.googleapis.com/css2?family=Gabarito:wght@400..900&display=swap");
/* Custom scrollbar for the horizontal task container */
::-webkit-scrollbar {
  height: 4px;
}
::-webkit-scrollbar-thumb {
  background: #a0aec0;
  border-radius: 2px;
}
.task-enter-active,
.task-leave-active {
  transition: all 1s ease;
}
.task-enter, .task-leave-to /* .task-leave-active in <2.1.8 */ {
  opacity: 0;
  transform: translateX(30px);
}
</style>
