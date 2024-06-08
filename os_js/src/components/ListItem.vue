<template>
    <div>
      <a
        v-if="item.type === 'default'"
        :href="item.href || '#'"
        @click.prevent="handleItemClick"
        :class="{ 'cursor-not-allowed opacity-50 pointer-events-none': item.disabled }"
        :aria-disabled="item.disabled"
        role="listitem"
      >
        {{ item.label }}
      </a>

      <label v-if="item.type === 'checkbox'" :class="{ 'cursor-not-allowed opacity-50 pointer-events-none': item.disabled }">
        <input type="checkbox" 
        :disabled="item.disabled" 
        @change="emitCheckboxChange" 
        :class="[checkboxColorClass,
        this.type === 'default' ? 'checkbox-input checkbox-blue' : 
        this.type === 'sky' ? 'checkbox-input checkbox-sky' :
        this.type === 'cyan' ? 'checkbox-input checkbox-cyan' :
        this.type === 'teal' ? 'checkbox-input checkbox-teal' :
        'checkbox-input checkbox-blue']"
        />
        <span class="ml-2"> {{ item.label }} </span>
      </label>

      <label v-if="item.type === 'toggle'" :class="[toggleContainerClasses, { 'cursor-not-allowed opacity-50 pointer-events-none': item.disabled }]">
        <input type="checkbox" 
        class="toggle-checkbox" 
        :disabled="item.disabled" 
        @change="emitToggleChange"
        :class="toggleColorClass"
        />
        <span> {{ item.label }} </span>
      </label>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ListItem',
    props: {
      item: {
        type: Object,
        required: true
      },
      type: {
        type: String,
        default: 'default'
      },
    },
    computed: {
      toggleContainerClasses() {
        return [
          'flex items-center space-x-2'
        ];
      },
      toggleColorClass() {
        switch (this.type) {
          case 'default':
            return 'checked:bg-blue-500';
          case 'sky':
            return 'checked:bg-sky-500';
          case 'cyan':
            return 'checked:bg-cyan-500';
          case 'teal':
            return 'checked:bg-teal-500';
          default:
            return 'checked:bg-blue-500';
        }
      },
      checkboxColorClass() {
        switch (this.type) {
          case 'default':
            return 'checked:bg-blue-500 text-blue-500';
          case 'sky':
            return 'checked:bg-sky-500 text-sky-500';
          case 'cyan':
            return 'checked:bg-cyan-500 text-cyan-500';
          case 'teal':
            return 'checked:bg-teal-500 text-teal-500';
          default:
            return 'checked:bg-blue-500 text-blue-500';
        }
      },
    },
    methods: {
      handleItemClick() {
        if (!this.item.disabled){
          this.$emit('item-click', this.item);
        }
      },
      emitToggleChange() {
        if (!this.item.disabled){
          this.$emit('toggle-change', this.item);
        }
      },
      emitCheckboxChange() {
        if (!this.item.disabled){
          this.$emit('checkbox-change', this.item);
        }
      }
    }
  }
</script>
  
<style scoped>
.checkbox-input {
  appearance: none;
  width: 16px;
  height: 16px;
  background-color: #fff;
  border-radius: 2px;
  display: inline-block;
  position: relative;
  vertical-align: middle;
}
.checkbox-input:checked:before {
  content: '';
  position: absolute;
  width: 5px;
  height: 9px;
  border: solid white;
  border-width: 0 2px 2px 0;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(45deg);
}
.checkbox-blue {
  border: 1px solid #4299E1;
}
.checkbox-sky {
  border: 1px solid #90CDF4;
}
.checkbox-cyan {
  border: 1px solid #81E6D9;
}
.checkbox-teal {
  border: 1px solid #4FD1C5;
}
.toggle-checkbox {
  appearance: none;
  width: 40px;
  height: 20px;
  background-color: #ccc;
  border-radius: 10px;
  position: relative;
  transition: background-color 0.2s;
}
.toggle-checkbox:before {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  background-color: white;
  border-radius: 50%;
  top: 1px;
  left: 1px;
  transition: transform 0.2s;
}

.toggle-checkbox:checked:before {
  transform: translateX(20px);
}
</style>