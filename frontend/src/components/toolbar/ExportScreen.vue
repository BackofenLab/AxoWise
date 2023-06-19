<template>
    <div class="tool-item">
        <li v-on:click="take_screen('white', 'png')">Save PNG (White)</li>
        <li v-on:click="take_screen('black', 'png')">Save PNG (Black)</li>
        <li v-on:click="take_screen('white', 'svg')">Save SVG (White)</li>
        <li v-on:click="take_screen('black', 'svg')">Save SVG (Black)</li>
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