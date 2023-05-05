<template>
    <div class="tool-item">
        <li v-on:click="take_screen('white')">Save Image White</li>
        <li v-on:click="take_screen('black')">Save Image Black</li>
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
        take_screen(mode){
            if(this.type == "protein"){
                this.emitter.emit("exportGraph", mode);
            }else {
                this.emitter.emit("exportTermGraph", mode);
            }
        }
    }
}
</script>