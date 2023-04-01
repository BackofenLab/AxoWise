<template>
    <div class="toolbar-connect">
        <span>DE Values</span>
        <div class="toolbar-theme">
            <v-select id="select_g" v-if="dcoloumns != null" v-model="selected_func" :options="dcoloumns" @update:model-value="show_whole"></v-select>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DEValue',
    data() {
        return {
            dcoloumns: this.$store.state.dcoloumns,
            selected_func: null,
        }
    },
    methods: {
        show_whole(value) {
            this.emitter.emit("decoloumn", value);
        }
    },
}
</script>