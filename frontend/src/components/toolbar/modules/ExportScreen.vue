<template>
    <div class="tool-item" v-on:mouseover="show_export=true"
        v-on:mouseleave="show_export=false">
        <span v-on:click="take_screen('white', 'png')">Save graph as</span>
        <div id="select-de">></div>
        <div class="subform-de-values" v-if="show_export">
        <span v-on:click="take_screen('white', 'png')">White/.png</span>
        <br>
        <span v-on:click="take_screen('black', 'png')">Black/.png</span>
        <br>
        <span v-on:click="take_screen('white', 'svg')">White/.svg</span>
        <br>
        <span v-on:click="take_screen('black', 'svg')">Black/.svg</span>
        </div>
    </div>
</template>

<script>

export default {
    name: 'ExportScreen',
    props: ['mode'],
    data() {
        return {
            show_export: false,
        }
    },
    methods: {
        take_screen(mode, format){
            this.emitter.emit("exportGraph", {params: {mode, format}, mode: this.mode});
        },
    }
}
</script>