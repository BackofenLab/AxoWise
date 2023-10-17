<template>
    <div class="tool-item">
        <span v-on:click="take_screen('white', 'png')">Save graph as</span>
        <!-- <span v-on:click="take_screen('black', 'png')">Save PNG (Black)</span>
        <span v-on:click="take_screen('white', 'svg')">Save SVG (White)</span>
        <span v-on:click="take_screen('black', 'svg')">Save SVG (Black)</span> -->
    </div>
</template>

<script>

export default {
    name: 'ExportScreen',
    props: ['type'],
    data() {
        return {
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