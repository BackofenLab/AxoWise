<template>
    <div class="tool-item">
        <li v-on:click="take_screen">Save Image...</li>
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
        take_screen(){
            if(this.type == "protein"){
                this.emitter.emit("exportGraph", "graph");
            }else {
                this.emitter.emit("exportTermGraph", "termgraph");
            }
        }
    }
}
</script>