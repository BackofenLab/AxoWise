<template >
    <div>
        <ul class="menu-bar">
            <li v-on:click="switch_home()">
                <img src="@/assets/toolbar/home.png" alt="Home Icon">
            </li>
            <li v-on:mouseover="search_active=true"
                v-on:mouseleave="search_active=false">
                <img src="@/assets/toolbar/search.png" alt="Search Icon">
            </li>
            <li v-on:mouseover="tools_active=true"
                v-on:mouseleave="tools_active=false">
                <img src="@/assets/toolbar/menu-burger.png" alt="Tool Icon">
            </li>
            <li v-on:click="switch_terms()">
                <img src="@/assets/toolbar/share.png" alt="Graph Icon">
            </li>
            <li v-on:click="center()">
                <img src="@/assets/toolbar/expand.png" alt="Center Icon">
            </li>
            <li v-on:click="threeview()">
                <img src="@/assets/toolbar/3d-icon.png" alt="3D Icon">
            </li>
        </ul>
        <div class="menu-window" v-show="tools_active == true" 
            v-on:mouseleave="tools_active = false;"
            v-on:mouseover="tools_active=true;">

            <div class="menu-items">
                <ExportScreen
                :type="screen_type"
                ></ExportScreen>
                <ExportGraph></ExportGraph>
                <NodeLabelSelect
                :type="screen_type"
                ></NodeLabelSelect>
                <ModuleSelection
                :type="screen_type"
                ></ModuleSelection>
                <ProteinList
                :protein_list='protein_list'
                @status_changed = 'status = $event'
                ></ProteinList>
                <SelectionWindow
                @selection_status_changed = 'selection_status = $event'
                ></SelectionWindow>
                <EdgeOpacity></EdgeOpacity>
                <DEValue></DEValue>

            </div>



        </div>
        <div class="search-window" v-show="search_active == true" 
            v-on:mouseleave="search_active = false;"
            v-on:mouseover="search_active=true;">

            <div class="search-item">
                <SearchBar
                :gephi_data='gephi_data'
                ></SearchBar>
            </div>
        </div>
        <div id="protein_highlight" v-show="status === true " class="highlight_list">
            <div id="protein_highlight_header">
                <div class="text">
                    <div class="headertext">
                        <span>Highlight Proteins</span>
                        <button v-on:click="status=false" id="highlight-btn-min"></button>
                    </div>
                </div>
            </div>
            <div class="highlight_main">
                <textarea v-model="raw_text" rows="10" cols="30" autofocus></textarea>
                <button v-on:click="highlight(raw_text)" id="highlight_protein">Go</button>
            </div>
        </div>
        <div id="selection_highlight" v-show="selection_status === true " class="highlight_list">
            <div id="selection_highlight_header">
                <div class="text">
                    <div class="headertext">
                        <span>Selection Window</span>
                        <button v-on:click="selection_status=false" id="highlight-btn-min"></button>
                    </div>
                </div>
            </div>
            <div class="highlight_main">
                <SelectionList
                :gephi_data='gephi_data'
                ></SelectionList>

            </div>
        </div>

    </div>
</template>

<script>

import ExportScreen from '@/components/toolbar/ExportScreen.vue'
import DEValue from '@/components/toolbar/DEValue.vue'
import ExportGraph from '@/components/toolbar/ExportGraph.vue'
import NodeLabelSelect from '@/components/toolbar/NodeLabelSelect.vue'
import ModuleSelection from '@/components/toolbar/ModuleSelection.vue'
import ProteinList from '@/components/toolbar/ProteinList.vue'
import SelectionWindow from '@/components/toolbar/SelectionWindow.vue'
import SearchBar from '@/components/toolbar/SearchBar.vue'
import EdgeOpacity from '@/components/toolbar/EdgeOpacity.vue'
import SelectionList from '@/components/toolbar/SelectionList.vue'

export default {
    name: 'MainToolBar',
    props: ['gephi_data'],
    emits:['active_subset_changed'],
    components: {
        ExportScreen,
        DEValue,
        ExportGraph,
        ProteinList,
        SelectionWindow,
        SearchBar,
        EdgeOpacity,
        SelectionList,
        NodeLabelSelect,
        ModuleSelection

    },
    data() {
        return {
            tools_active: false,
            search_active: false,
            screen_type: "protein",
            snapshot: null,
            status: false,
            raw_text: "",
            selection_status: false,
            protein_list: null,
        }
    },
    methods: {
        switch_terms() {
            if(this.$store.state.term_graph_data != null){
                this.$router.push("terms")
            }
        },
        switch_home() {
            this.$router.push('/').then(() => {
                window.location.reload();
            });
        },
        highlight(proteins) {
            var com = this

            const protein_names = new Set(proteins.toUpperCase().split("\n"))
            const subset = []
            com.gephi_data.nodes.forEach(node => {
                if(protein_names.has(node.attributes['Name'])){
                    subset.push(node)
                }
            });

            com.$emit("active_subset_changed", subset);
        },
        center() {
            this.emitter.emit("centerGraph", true);
        },
        threeview() {
            this.emitter.emit("threeView");
        }
    }
}
</script>

<style>
.menu-bar {
    position: fixed;
	border-radius: 25px;
	height: fit-content;
	display: inline-flex;
	background-color: hsla(0,0%,100%,.15);
    backdrop-filter: blur(10px);  
	-webkit-backdrop-filter: blur(10px);
	align-items: center;
	padding: 0 10px;
	margin: 10px 0 0 0;
    z-index: 99;
}
.menu-bar li {
    list-style: none;
    color: white;
    font-family: sans-serif;
    font-weight: bold;
    padding: 12px;
    margin: 0 8px;
    position: relative;
    cursor: pointer;
    white-space: nowrap;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
}
.menu-bar li::before {
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
.menu-bar li:hover::before {
	background: linear-gradient(to bottom, #e8edec, #d2d1d3);
	box-shadow: 0px 3px 20px 0px black;
	transform: scale(1.2);
}
.menu-bar li:hover {
	color: black;
}
/* Use ::v-deep to apply styles to nested child components */
::v-deep .menu-bar li {
	color: white;
}
::v-deep .menu-bar li:hover {
	color: black;
}

.menu-window {
    background-color: hsla(0,0%,100%,.1);
	-webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);  
    width: 280px;
    margin: 10px 0 0 17.5px;
    height: 600px;
    position: fixed;
    border-radius: 20px;
    justify-content: center;
}

.search-window {
    background-color: hsla(0,0%,100%,.1);
	-webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);  
    width: 280px;
    margin: 10px 0 0 17.5px;
    height: 400px;
    position: fixed;
    border-radius: 20px;
    justify-content: center;
}

.menu-items {
    margin-top: 50px;
    width: 100%;
    text-align: center;
    color: white;
}

.search-item {
    display: flex;
    position: relative;
    margin-top: 50px;
    width: 100%;
    align-content: center;
    justify-content: center;
}

.menu-bar li img {
    width: 30px;
    filter: invert(1);
}

.menu-bar li:hover img {
    filter: invert(0);
}
</style>
