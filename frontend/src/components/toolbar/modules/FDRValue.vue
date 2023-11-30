<template>
    <div class="tool-item">
        <span>Visualize fdr-rate</span>
        <button v-on:click="activate_fdr(check);check=!check" id="activate-fdr">yes</button>
    </div>
</template>

<script>

export default {
    name: 'FDRValue',
    data() {
        return {
            check: true,
        }
    },
    methods: {
        activate_fdr(){
            this.emitter.emit("activateFDR", this.check);
        }
    }
}
</script>

<style>

#activate-fdr {
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