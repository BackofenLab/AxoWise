<template>
    <div class="tool-item">
        <li v-on:click="reset_labels">Deactivate module selection</li>
    </div>
</template>

<script>

export default {
    name: 'ModuleSelection',
    props: ['type'],
    data() {
        return {
        }
    },
    methods: {
        reset_labels(){
            if(this.type == "protein"){
                this.emitter.emit("deactivateModules");
            }
        }
    }
}
</script>