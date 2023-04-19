<template >
    <div>
        <ul class="term-menu-bar">
            <li v-on:mouseover="search_active=true"
                v-on:mouseleave="search_active=false">S</li>
            <li v-on:mouseover="tools_active=true"
                v-on:mouseleave="tools_active=false">T</li>
            <li v-on:click="switch_terms()">G</li>
            <li v-on:click="center()">C</li>
        </ul>
        <div class="term-menu-window" v-show="tools_active == true" 
            v-on:mouseleave="tools_active = false;"
            v-on:mouseover="tools_active=true;">

            <div class="menu-items">
                <ExportScreen :type="screen_type"></ExportScreen>
                <FDRValue></FDRValue>
                <TermConnectedGraph></TermConnectedGraph>
            </div>



        </div>
        <div class="term-search-window" v-show="search_active == true" 
            v-on:mouseleave="search_active = false;"
            v-on:mouseover="search_active=true;">

            <div class="term-search-item">
                <TermSearch
                :term_data='term_data'
                ></TermSearch>
            </div>
        </div>
    </div>
</template>

<script>

import ExportScreen from '@/components/toolbar/ExportScreen.vue'
import TermConnectedGraph from '@/components/term_graph/TermConnectedGraph.vue'
import TermSearch from '@/components/term_graph/TermSearch.vue'
import FDRValue from '@/components/term_graph/FDRValue.vue'

export default {
    name: 'TermToolBar',
    props: ['term_data'],
    emits:[],
    components: {
        ExportScreen,
        TermConnectedGraph,
        TermSearch,
        FDRValue

    },
    data() {
        return {
            tools_active: false,
            screen_type: "term",
            search_active: false,
        }
    },
    methods: {
        switch_terms() {
            this.$router.push("protein")
        },
        center() {
            this.emitter.emit("centerTermGraph", true);
        }
    }
}
</script>

<style>
.term-menu-bar {
    position: fixed;
	border-radius: 25px;
	height: fit-content;
	display: inline-flex;
    width: 350px;
	background-color: hsla(0,0%,100%,.15);
    backdrop-filter: blur(10px);  
	-webkit-backdrop-filter: blur(10px);
	align-items: center;
	padding: 0 10px;
	margin: 10px 0 0 0;
    z-index: 99;
}
.term-menu-bar li {
	list-style: none;
	color: white;
	font-family: sans-serif;
	font-weight: bold;
	padding: 12px 16px;
	margin: 0 8px;
	position: relative;
	cursor: pointer;
	white-space: nowrap;
}
.term-menu-bar li::before {
	content: " ";
	position: absolute;
	top: 0;
	left:0;
	height:100%;
	width: 100%;
	z-index:-1;
	transition: .2s;
	border-radius: 25px;
}
.term-menu-bar li:hover::before {
	background: linear-gradient(to bottom, #e8edec, #d2d1d3);
	box-shadow: 0px 3px 20px 0px black;
	transform: scale(1.2);
}
.term-menu-bar li:hover {
	color: black;
}
/* Use ::v-deep to apply styles to nested child components */
::v-deep .term-menu-bar li {
	color: white;
}
::v-deep .term-menu-bar li:hover {
	color: black;
}

.term-menu-window {
    background-color: hsla(0,0%,100%,.1);
	-webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);  
    width: 310px;
    margin: 10px 0 0 17.5px;
    height: 600px;
    position: fixed;
    border-radius: 20px;
    justify-content: center;
}

.term-search-window {
    background-color: hsla(0,0%,100%,.1);
	-webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);  
    width: 310px;
    margin: 10px 0 0 17.5px;
    height: 400px;
    position: fixed;
    border-radius: 20px;
    justify-content: center;
}

.term-search-item {
    display: flex;
    margin: 50px;
    align-content: center;
    justify-content: center;
}
</style>
