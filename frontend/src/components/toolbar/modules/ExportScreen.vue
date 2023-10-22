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
    data() {
        return {
            show_export: false,
            type: 'protein'
        }
    },
    methods: {
        take_screen(mode, format){
            if(this.type == "protein"){
                this.emitter.emit("exportGraph", {mode, format});
            }else {
                this.emitter.emit("exportTermGraph", {mode, format});
            }
        },
    }
}
</script>