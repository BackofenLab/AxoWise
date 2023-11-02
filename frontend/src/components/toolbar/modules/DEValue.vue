<template>
    <div class="tool-item" v-on:mouseover="show_subselection=true"
    v-on:mouseleave="show_subselection=false">
                
        <span>Coloumns</span>
        <span class="selected-de" v-if="selected_func !== null">({{ selected_func }})</span>
        <div id="select-de">></div>
        <div class="subform-de-values" v-if="show_subselection && dcoloumns">
            <div class="de-coloumn-values" v-for="(entry, index) in dcoloumns" :key="index" v-on:click="show_whole(entry)" :class="{selectedde: selected_func == entry}">
                <a>{{ entry }}</a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DEValue',
    data() {
        return {
            dcoloumns: this.$store.state.dcoloumns,
            selected_func: null,
            show_subselection: false
        }
    },
    methods: {
        show_whole(value) {
            this.selected_func = value
            this.emitter.emit("decoloumn", value);
        },
    },

    mounted() {
        this.emitter.on("reset_decoloumn", () => {
            this.selected_func = null
        });
    }
}
</script>

<style>
#select-de {
	width: 9%;
    height: 6%;
	position: absolute;
    right:6.3%;
	cursor: pointer;
    border: none;
	border-radius: 5px;
	color: white;
    font-family: 'ABeeZee', sans-serif;
    font-size: 1.2vw;
    text-align: center;
}

.subform-de-values{
    position: fixed;
    margin-top: -0.3%;
    left: 25.4%;
    width: auto;
    height: auto;
    font-size: 0.9vw;
    padding: 0.5vw;
    border-style: solid;
    border-width: 1px;
    border-color: #0A0A1A;
    background: rgba(222, 222, 222, 0.61);
    border-radius: 5px;
    text-align: left;
    overflow: hidden;
    cursor: default;
}

.de-coloumn-values{
    padding: 0.1vw;
}

.selectedde {
    background-color: #0A0A1A;
    border-radius: 5px;
}
.selected-de{
    margin-left: 0.4vw;
}

</style>