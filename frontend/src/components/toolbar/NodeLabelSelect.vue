<template>
    <div class="tool-item">
        <li v-on:click="reset_labels">Reset Label...</li>
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