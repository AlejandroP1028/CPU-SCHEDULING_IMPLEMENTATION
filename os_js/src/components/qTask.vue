<template>
    <div  data-popover-target="popover-default" class="border flex justify-center border-gray-900">
        <p class="text-lg font-medium" @hover="showPopover"> {{task.id}}</p>
        
    </div>
    <div data-popover id="popover-default" role="tooltip" class="absolute z-10 invisible inline-block w-64 text-sm text-gray-500 transition-opacity duration-300 bg-white border border-gray-200 rounded-lg shadow-sm opacity-0 dark:text-gray-400 dark:border-gray-600 dark:bg-gray-800">
        <div class="px-3 py-2 bg-gray-100 border-b border-gray-200 rounded-t-lg dark:border-gray-600 dark:bg-gray-700">
            <h3 class="font-semibold text-gray-900 dark:text-white">Popover title</h3>
        </div>
        <div class="px-3 py-2">
            <p>And here's some amazing content.  It's very engaging. Right?</p>
        </div>
        <div data-popper-arrow></div>
    </div>
</template>

<script>

export default{
    name: 'q-task',

    props: {
        task: Object
    }

}
</script>

<style scoped>
</style>