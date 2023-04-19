<template>
    <div class="toolbar-connect">
        <span>ConnectedGraph</span>
        <div class="toolbar-theme">
            <v-select id="select_g" v-model="selected_func" :options="select_function" @update:model-value="show_whole"></v-select>
        </div>
    </div>
</template>

<script>

export default {
    name: 'TermConnectedGraph',
    data() {
        return {
            select_function: ["Whole Graph", "Main Graph"],
            selected_func: null
        }
    },
    methods: {
        show_whole(value) {
            this.emitter.emit("unconnectedTermGraph", value);
        }
    }
}
</script>

<style>
    .toolbar-connect {
        border-style: outset;
        border-width: 1px;
        margin: 5px;
        height: 100px;
        border-radius: 20px;
    }
</style>