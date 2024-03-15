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

<style>
.subform-de-values{
    position: fixed;
    margin-top: -0.3%;
    left: 49.4%;
    width: auto;
    height: auto;
    font-size: 0.9vw;
    padding: 0.5vw;
    border-style: solid;
    border-width: 1px;
    border-color: #0A0A1A;
    background: rgba(222, 222, 222, 0.61);
    border-radius: 5px;
    text-align: left;
    overflow: hidden;
    cursor: default;
}
</style>