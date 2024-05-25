<template>
    <div class="border flex justify-center border-gray-900">
        <p class="text-lg font-medium" @hover="showPopover"> {{id}}</p>
        <popover/>
    </div>
</template>

<script>

export default{
    name: 'pop-over',

    props: {
        arrivalTime: Number,
        cpuBurst: Number
    }

}
</script>

<style scoped>
</style>