<template>
  <div :class="['rounded-lg shadow', computedClassesMain]">
    {{ text }}
  </div>
</template>

<script>
export default {
  name: 'CardComponent',
  props: {
    text: String,
  },
  computed: {
    computedClassesMain() {
    }
  }
}
</script>

<style scoped>
/* Add any scoped styles if needed */
</style>
