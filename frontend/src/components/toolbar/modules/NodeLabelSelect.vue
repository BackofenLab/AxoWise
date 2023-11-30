<template>
    <div class="tool-item">
        <span>Reset labels</span>
        <button v-on:click="reset_labels()" id="reset-labels">yes</button>
    </div>
</template>

<script>

export default {
    name: 'NodeLabelSelect',
    props: ['mode'],
    data() {
        return {
        }
    },
    methods: {
        reset_labels(){
            console.log(this.mode)
            this.emitter.emit("resetSelect", {mode: this.mode});
        }
    }
}
</script>

<style>

#reset-labels {
	width: 9%;
    height: 6%;
	position: absolute;
    right:6.3%;
	margin-top: 0.1vw;
	background-color: #ddd;
	cursor: pointer;
    border: none;
	border-radius: 5px;
	color: #0A0A1A;
    font-family: 'ABeeZee', sans-serif;
    font-size: 0.7vw;
    text-align: center;
}
</style>