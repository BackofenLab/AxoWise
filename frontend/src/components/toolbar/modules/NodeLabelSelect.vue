<template>
    <div class="tool-item">
        <span v-on:click="reset_labels">Reset Label...</span>
    </div>
</template>

<script>

export default {
    name: 'NodeLabelSelect',
    props: ['type'],
    data() {
        return {
        }
    },
    methods: {
        reset_labels(){
            if(this.type == "protein"){
                this.emitter.emit("resetSelect");
            }else {
                this.emitter.emit("resetTermSelect")
            }
        }
    }
}
</script>