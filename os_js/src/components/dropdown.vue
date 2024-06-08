<template>
    <div class="relative">
      <div>
        <button @click="toggleDropdown" 
        :class="[buttonClasses, { 'cursor-not-allowed opacity-50': disabled }]" 
        :disabled="disabled" 
        type="button"
        class="text-white border-white">
  {{ buttonText }}
  <svg class="inline-block ml-2" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M7 10l5 5 5-5H7z" fill="currentColor"/>
  </svg>
</button>


      </div>
      <transition :name="[this.menuAlignment === 'center' ? 'center' : 'v']">
        <div v-if="show" :class="dropdownClasses">
          <template v-for="(item, index) in menuItems" :key="index">
            <ListItem 
              :item="item"
              :type="type"
              @item-click="handleListItemClick"
              @toggle-change="handleToggleChange"
              @checkbox-change="handleCheckboxChange"
              :class="itemClasses"
            ></ListItem>
            <div v-if="item && item.divider" :class="setDivider(item.customMargin)"></div>
            <div v-if="divider && index < menuItems.length - 1" :class="setDivider(item.customMargin)"></div>
          </template>
        </div>
      </transition>
    </div>
  </template>
  
  <script>
  import ListItem from './ListItem.vue';
  export default {
    name: 'DropdownComponent',
    components: {
      ListItem
    },
    props: {
      type: {
        type: String,
        validator: function (value) {
          return ['default', 'sky', 'cyan', 'teal'].includes(value);
        },
        default: 'default'
      },
      buttonText: {
        type: String,
        default: 'Dropdown',
      },
      size: {
        type: String,
        validator: function (value) {
          return ['w', 's', 'm', 'l'].includes(value);
        },
        default: 'w',
      },
      menuWidth: {
        type: String,
        default: 'full',
        validator: function (value) {
          return ['auto', 'full', 'w-48', 'w-64'].includes(value);
        }
      },
      menuAlignment: {
        type: String,
        default: 'right',
        validator: function (value) {
          return ['left', 'center', 'right'].includes(value);
        }
      },
      bordered: {
        type: Boolean,
        default: false,
      },
      disabled: {
        type: Boolean,
        default: false
      },
      divider: {
        type: Boolean,
        default: false
      },
      menuItems: {
        type: Array,
        default: () => []
      }
    },
    data() {
      return {
        show: false
      }
    },
    computed: {
      sizeClass() {
        switch (this.size) {
          case 'w':
            return 'text-xs';
          case 's':
            return 'text-sm';
          case 'm':
            return 'text-base';
          case 'l':
            return 'text-lg';
          default:
            return 'text-xs';
        }
      },
      alignmentClass() {
        switch (this.menuAlignment) {
          case 'left':
            return 'left-0';
          case 'center':
            return 'left-1/2 transform -translate-x-1/2';
          case 'right':
            return 'right-0';
          default:
            return 'right-0';
        }
      },
      buttonClasses() {
        return [
          'inline-flex justify-center w-full rounded-2xl shadow-none px-4 py-2 font-medium focus:outline-none border-2 border-white',
          this.sizeClass
        ];
      },
      dropdownClasses() {
        const styleClasses = {
          default: {
            bgClass: 'dark:bg-gray-700 dark:text-blue-100 bg-blue-100 text-blue-800',
            borderClass: this.bordered ? 'border border-blue-300' : '',
          },
          sky: {
            bgClass: 'dark:bg-gray-700 dark:text-sky-100 bg-sky-100 text-sky-800',
            borderClass: this.bordered ? 'border border-sky-300' : '',
          },
          cyan: {
            bgClass: 'dark:bg-gray-700 dark:text-cyan-100 bg-cyan-100 text-cyan-800',
            borderClass: this.bordered ? 'border border-cyan-300' : '',
          },
          teal: {
            bgClass: 'dark:bg-gray-700 dark:text-teal-100 bg-teal-100 text-teal-800',
            borderClass: this.bordered ? 'border border-teal-300' : '',
          }
        };
  
        const { bgClass, borderClass } = styleClasses[this.type] || styleClasses['default'];
  
        return [
          'absolute origin-top-right mt-2 rounded-md shadow-lg z-10 max-h-60 overflow-auto py-2',
          bgClass, borderClass, this.alignmentClass,
          this.menuWidth === 'full' ? 'w-full' : this.menuWidth,
        ];
      },
      itemClasses() {
        return [
          'block px-4 py-2',
          this.sizeClass,
          this.type === 'default' ? 'hover:bg-blue-200 dark:hover:bg-gray-600' :
          this.type === 'sky' ? 'hover:bg-sky-200 dark:hover:bg-gray-600' :
          this.type === 'cyan' ? 'hover:bg-cyan-200 dark:hover:bg-gray-600' :
          this.type === 'teal' ? 'hover:bg-teal-200 dark:hover:bg-gray-600' :
          ''
        ];
      }
    },
    methods: {
      toggleDropdown() {
        this.show = !this.show;
      },
      closeDropdown() {
        this.show = false;
      },
      setDivider(a) {
        const styleClasses = {
          default: {
            borderClass: 'dark:border-blue-300/[.87] border-blue-300/[.87]',
          },
          sky: {
            borderClass: 'dark:border-sky-300/[.87] border-sky-300/[.87]',
          },
          cyan: {
            borderClass: 'dark:border-cyan-300/[.87] border-cyan-300/[.87]',
          },
          teal: {
            borderClass: 'dark:border-teal-300/[.87] border-teal-300/[.87]',
          }
        };
  
        const { borderClass } = styleClasses[this.type] || styleClasses['default'];
  
        return [
          'border-t-2',
          borderClass,
          a === '0.5' ? 'my-0.5' :
          a === '1' ? 'my-1' :
          a === '2' ? 'my-2' :
          'my-0.5'
        ];
      },
      handleListItemClick(item) {
        if(!item.disabled){
          this.$emit('list-item-click', item);
        }
      },
      handleToggleChange(item) {
        if(!item.disabled){
          this.$emit('toggle-change', item);
        }
      },
      handleCheckboxChange(item) {
        if(!item.disabled){
          this.$emit('checkbox-change', item);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .v-enter-active,
  .v-leave-active {
    transition: opacity 0.5s ease, transform 0.5s ease;
  }
  
  .v-enter-from,
  .v-leave-to {
    opacity: 0;
    transform: translateY(-5%);
  }
  .center-enter-active,
  .center-leave-active {
    transition: opacity 0.5s ease, transform 0.5s ease;
  }
  
  .center-enter-from,
  .center-leave-to {
    opacity: 0;
    transform: translateY(-50%,-5%);
  }
  </style>
  
