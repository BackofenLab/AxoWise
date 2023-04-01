<template>
    <div class="tool-item">
        <li v-on:click="take_screen">Save Image...</li>
    </div>
</template>

<script>

export default {
    name: 'ExportScreen',
    emits: [],
    data() {
        return {
        }
    },
    methods: {
        take_screen(){
            this.emitter.emit("exportGraph", "graph");
        }
    }
}
</script>