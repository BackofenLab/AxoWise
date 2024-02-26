<template>
        <div class="tool-item">
        <div id="selection_highlight" class="window-menu">
            <div class="selection_list">
                <div class="window-label">degree value</div>
                <div class="menu-items">
                    <div id="degree"></div>
                    <input
                        type="number"
                        v-bind:min="degree_boundary.min" v-bind:max="degree_boundary.max" v-bind:step="degree_boundary.step"
                        v-model="degree_boundary.minValue"
                        v-on:change="searchSubset()"
                        v-on:input="valueChanged('degree', [degree_boundary.minValue,degree_boundary.maxValue])"
                    />
                    <span class="seperator">-</span>
                    <input
                        type="number"
                        v-bind:min="degree_boundary.min" v-bind:max="degree_boundary.max" v-bind:step="degree_boundary.step"
                        v-model="degree_boundary.maxValue"
                        v-on:change="searchSubset()"
                        v-on:input="valueChanged('degree', [degree_boundary.minValue,degree_boundary.maxValue])"
                    />
                </div>
                <div class="window-label">betweenness centrality value</div>
                <div class="menu-items">
                    <div id="betweenes"></div>
                    <input
                        type="number"
                        v-bind:min="bc_boundary.min" v-bind:max="bc_boundary.max" v-bind:step="bc_boundary.step"
                        v-model="bc_boundary.minValue"
                        v-on:change="searchSubset()"
                        v-on:input="valueChanged('betweenes',[bc_boundary.minValue, bc_boundary.maxValue])"
                    />
                    <span class="seperator">-</span>
                    <input
                        type="number"
                        v-bind:min="bc_boundary.min" v-bind:max="bc_boundary.max" v-bind:step="bc_boundary.step"
                        v-model="bc_boundary.maxValue"
                        v-on:change="searchSubset()"
                        v-on:input="valueChanged('betweenes',[bc_boundary.minValue, bc_boundary.maxValue])"
                    />
                </div>
                <div v-if="mode=='term'">
                    <div class="window-label">padj value</div>
                    <div class="menu-items">
                        <input 
                            id="padj"
                            type="range"
                            v-bind:min="padj_boundary.min" v-bind:max="padj_boundary.max" v-bind:step="padj_boundary.step"
                            v-model="padj_boundary.value"
                            v-on:change="searchSubset()"
                            v-on:input="valueChanged('padj')"
                        />
                        <!-- <input 
                            type="number"
                            v-bind:min="padj_boundary.min" v-bind:max="padj_boundary.max" v-bind:step="padj_boundary.step"
                            v-model="padj_boundary.value"
                            v-on:change="searchSubset()"
                            v-on:input="valueChanged('padj')"
                        /> -->
                    </div>
                </div>
                <div class="window-label">page rank value</div>
                <div class="menu-items">
                    <div id="pagerank"></div>
                    <input 
                        type="number"
                        v-bind:min="pr_boundary.min" v-bind:max="pr_boundary.max" v-bind:step="pr_boundary.step"
                        v-model="pr_boundary.minValue"
                        v-on:change="searchSubset()"
                        v-on:input="valueChanged('pagerank',[pr_boundary.minValue, pr_boundary.maxValue])"
                    />
                    <span class="seperator">-</span>
                    <input 
                        type="number"
                        v-bind:min="pr_boundary.min" v-bind:max="pr_boundary.max" v-bind:step="pr_boundary.step"
                        v-model="pr_boundary.maxValue"
                        v-on:change="searchSubset()"
                        v-on:input="valueChanged('pagerank',[pr_boundary.minValue, pr_boundary.maxValue])"
                    />
                </div>
                <div class="dcoloumn-window"  v-if="dcoloumns">
                <div class="class-section" v-on:click="coloumnsCheck = !coloumnsCheck">
                    <span>coloumn section</span>
                    <img src="@/assets/pane/invisible.png" v-if="!coloumnsCheck">
                    <img src="@/assets/pane/visible.png" v-if="coloumnsCheck">
                </div>
                <div class="d-section-slider" v-show="coloumnsCheck" v-for="(entry, index) in dcoloumns" :key="index">
                <div class="window-label">{{ entry }}</div>
                    <div class="menu-items">
                        <div :id="'deval-slider-' + index"></div>
                        <input 
                        type="number"
                        v-bind:min="dboundaries[entry].min" v-bind:max="dboundaries[entry].max" v-bind:step="dboundaries[entry].step"
                        v-model="dboundaries[entry].minValue"
                        v-on:change="searchSubset()"
                        v-on:input="valueChanged('deval-slider-' + index,[dboundaries[entry].minValue, dboundaries[entry].maxValue])"
                        />
                        <span class="seperator">-</span>
                        <input 
                            type="number"
                            v-bind:min="dboundaries[entry].min" v-bind:max="dboundaries[entry].max" v-bind:step="dboundaries[entry].step"
                            v-model="dboundaries[entry].maxValue"
                            v-on:change="searchSubset()"
                            v-on:input="valueChanged('deval-slider-' + index,[dboundaries[entry].minValue, dboundaries[entry].maxValue])"
                        />
                    </div>
                </div>  
            </div>
            </div>
            <div id="selection_highlight_header" class="window-header">
                <div class="headertext">
                    <span>graph parameter</span>
                    <img  class="protein_close" src="@/assets/pathwaybar/cross.png" v-on:click="unactive_proteinlist()">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import * as noUiSlider from 'nouislider';
import '@/slider.css';

export default {
    name: 'SelectionList',
    props: ['data','mode','active_subset', 'active_term'],
    emits: ['selection_active_changed'],
    data() {
        return {
            once: true,
            search_data: null,
            coloumnsCheck:false,
			degree_boundary: { minValue: 0, maxValue: 0, min: 0, max: Number, step: 1},
            pr_boundary: { minValue: 0, maxValue: 0, min: 0, max: Number, step: 0.01},
            bc_boundary: { minValue: 0, maxValue: 0, min: 0, max: Number, step: 1},
            padj_boundary: { value: 0, min: 0, max: 1000, step: 1},
            dcoloumns: this.$store.state.dcoloumns,
            dboundaries: {},
            nodeCheck: false,
            formatType: null
        }
    },
    watch: {
        active_subset(){
            if(!this.active_subset) {
                this.unactive_proteinlist()
                return
            }
            if(!this.active_subset.selection) this.unactive_proteinlist()
        },
        active_term(){
            this.unactive_proteinlist()
        }
    },
    methods: {
        initialize_de(){
            var com = this;
            var dataForm = com.data;

            for (var coloumn of this.dcoloumns){

                // _____ this calculation has only to be done once _______
                var subset_de
                subset_de = dataForm.nodes.map(arrayItem => {
                    return arrayItem.attributes[coloumn]
                });
    
                // Convert String values to Integers
                var result = subset_de.map(function (x) { 
                    return parseFloat(x);
                });
                var maxDe = Math.max(...result);
                var minDe = Math.min(...result);
    
                this.dboundaries[coloumn] = {minValue:minDe, maxValue:maxDe, min: minDe, max: maxDe, step:0.01}

            }

        },
        create_de(){
            var com = this;

            Object.entries(com.dcoloumns).forEach(([index, coloumn]) => {

                var slider = document.getElementById('deval-slider-' + index);
                noUiSlider.create(slider, {
                    start: [com.dboundaries[coloumn].min, com.dboundaries[coloumn].max],
                    connect: true,
                    range: {
                        'min': com.dboundaries[coloumn].min,
                        'max': com.dboundaries[coloumn].max
                    },
                    step: 0.01
                });
    
                slider.noUiSlider.on('update', function (values, handle) {
                    com.dboundaries[coloumn][(handle ? "maxValue" : "minValue")] = values[handle];
                    com.searchSubset()
                    
                });

            });

            
        },
        dragElement(elmnt) {

            var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
            if (document.getElementById(elmnt.id + "_header")) {
                // if present, the header is where you move the DIV from:
                document.getElementById(elmnt.id + "_header").onmousedown = dragMouseDown;
            } else {
                // otherwise, move the DIV from anywhere inside the DIV: 
                elmnt.onmousedown = dragMouseDown;
            }

            function dragMouseDown(e) {
                e = e || window.event;
                e.preventDefault();
                // get the mouse cursor position at startup:
                pos3 = e.clientX;
                pos4 = e.clientY;
                document.onmouseup = closeDragElement;
                // call a function whenever the cursor moves:
                document.onmousemove = elementDrag;
            }

            function elementDrag(e) {
                e = e || window.event;
                e.preventDefault();
                // calculate the new cursor position:
                pos1 = pos3 - e.clientX;
                pos2 = pos4 - e.clientY;
                pos3 = e.clientX;
                pos4 = e.clientY;
                // set the element's new position:
                elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
                elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
            }

            function closeDragElement() {
                // stop moving when mouse button is released:
                document.onmouseup = null;
                document.onmousemove = null;
            }
        },
		initialize_dg: function() {
			var com = this;

			var dataForm = com.data;

			// initialize values of slider
            var subset_degree;

            subset_degree = dataForm.nodes.map(arrayItem => {
                return arrayItem.attributes["Degree"]
            });

            // Convert String values to Integers
            var result = subset_degree.map(function (x) { 
                return parseInt(x, 10);
            });

            var maxDeg = Math.max(...result);        // Need to use spread operator!

            var slider = document.getElementById('degree');
            noUiSlider.create(slider, {
                start: [0, maxDeg],
                connect: true,
                range: {
                    'min': 0,
                    'max': maxDeg
                },
                format: this.formatType,
                step: 1
            });

            slider.noUiSlider.on('update', function (values, handle) {
                com.degree_boundary[(handle ? "maxValue" : "minValue")] = values[handle];
                com.searchSubset()
                
            });
		},
        initialize_bc() {
            var com = this;

            var dataForm = com.data;

            // _____ this calculation has only to be done once _______
            var subset_bc
            subset_bc = dataForm.nodes.map(arrayItem => {
                return arrayItem.attributes["Betweenness Centrality"]
            });

            // Convert String values to Integers
            var result = subset_bc.map(function (x) { 
                return parseFloat(x, 10);
            });
            var maxDeg = Math.max(...result) + 10;       // Need to use spread operator!

            var slider = document.getElementById('betweenes');
            noUiSlider.create(slider, {
                start: [0, maxDeg],
                connect: true,
                range: {
                    'min': 0,
                    'max': maxDeg
                },
                format: this.formatType,
                step: 1
            });

            slider.noUiSlider.on('update', function (values, handle) {
                com.bc_boundary[(handle ? "maxValue" : "minValue")] = values[handle];
                com.searchSubset()
                
            });

        },
        initialize_pagerank() {
            var com = this;

            var dataForm = com.data;

            // _____ this calculation has only to be done once _______
            var subset_pr
            subset_pr = dataForm.nodes.map(arrayItem => {
                return arrayItem.attributes["PageRank"]
            });

            // Convert String values to Integers
            var result = subset_pr.map(function (x) { 
                return parseFloat(x);
            });
            var maxDeg = Math.abs(Math.log10(Math.min(...result)))+1;   // Need to use spread operator!


            this.pr_boundary.max = maxDeg;
            var slider = document.getElementById('pagerank');
            noUiSlider.create(slider, {
                start: [0, maxDeg],
                connect: true,
                range: {
                    'min': 0,
                    'max': maxDeg
                },
                step: 0.01
            });

            slider.noUiSlider.on('update', function (values, handle) {
                com.pr_boundary[(handle ? "maxValue" : "minValue")] = values[handle];
                com.searchSubset()
                
            });

        },
        searchSubset() {
            var com = this

            var dataForm = com.search_data;
            // filter hubs
			var finalNodes = [];
			var nodes = [];
			// degree filtering
			for (var element of dataForm){
				if(parseInt(element.attributes["Degree"]) >= this.degree_boundary.minValue &&
                   parseInt(element.attributes["Degree"]) <= this.degree_boundary.maxValue &&
                   Math.abs(Math.log10(parseFloat(element.attributes["PageRank"]))) >= this.pr_boundary.minValue &&
                   Math.abs(Math.log10(parseFloat(element.attributes["PageRank"]))) <= this.pr_boundary.maxValue &&
                   parseFloat(element.attributes["Betweenness Centrality"]) >= this.bc_boundary.minValue &&
                   parseFloat(element.attributes["Betweenness Centrality"]) <= this.bc_boundary.maxValue
                   ){
                    if(com.mode=='term'){
                        if(Math.abs(Math.log10(element.attributes["FDR"])) >= com.padj_boundary.value) nodes.push(element)
                    }
                    else if (this.dcoloumns) {
                        this.nodeCheck = true
                        for (var coloumn of com.dcoloumns){
                            if(parseFloat(element.attributes[coloumn]) < com.dboundaries[coloumn].minValue || 
                               parseFloat(element.attributes[coloumn]) > com.dboundaries[coloumn].maxValue){
                                this.nodeCheck = false
                                break;
                            }
                        }
                        if(this.nodeCheck) nodes.push(element)
                        
                    }
                    else{
                        nodes.push(element)
                    }
				}
			}
			finalNodes = nodes;
			this.emitter.emit("searchSubset", {subset:{selection: true, genes:finalNodes}, mode:this.mode});
        },
        unactive_proteinlist(){
            this.$emit("selection_active_changed", false);
            // if(this.active_subset) this.emitter.emit("searchSubset", {subset:this.search_data, mode:this.mode});
        },
        valueChanged(id, value){
            var slider = document.getElementById(id)
            slider.noUiSlider.set(value);
        },
        term_genes(list){
            var term_genes = new Set(list)
            var termlist = this.data.nodes.filter(element => term_genes.has(element.attributes["Name"]))
            return termlist
        }
	},
    mounted(){

        this.formatType = {
            from: function(value) {
                return parseInt(value);
            },
            to: function(value) {
                return parseInt(value);
            }
        }
    
        if(this.mode=="protein"){
            this.search_data = this.$store.state.active_subset ? this.term_genes(this.$store.state.active_subset): this.data.nodes
        }else {
            this.search_data = this.$store.state.p_active_subset ? this.term_genes(this.$store.state.p_active_subset): this.data.nodes
        }
        this.dragElement(document.getElementById("selection_highlight"));

        this.initialize_dg()
        this.initialize_bc()
        this.initialize_pagerank()
        if (this.dcoloumns) this.create_de()

        
    },
    created() {
        if (this.dcoloumns) this.initialize_de()
    }
}
</script>

<style>

.selection_list {
    position: absolute;
    top: 9.41%;
    width: 100%;
    height: 12vw;
    padding-top: 3%;
    border-radius: 0px 0px 5px 5px;
    background: rgba(222, 222, 222, 0.61);
    backdrop-filter: blur(7.5px);
    overflow-y: scroll;
    overflow-x: hidden;
}
.selection_list .menu-items{
    display: flex;
}
/* Hide scrollbar for Chrome, Safari and Opera */
.selection_list::-webkit-scrollbar {
    display: none;
}

.selection_list .window-label {
    color: white;
    white-space: nowrap;
    overflow-x: hidden;    /* Hide overflow content */
    text-overflow: ellipsis;
}
#degree {
    margin:0.5vw 0.5vw 0.5vw 0;
}

#betweenes {
    margin:0.5vw 0.5vw 0.5vw 0;
}

#pagerank {
    margin:0.5vw 0.5vw 0.5vw 0;
}

[id^="deval-slider-"]{
    margin:0.5vw 0.5vw 0.5vw 0;
}

.selection_list input[type=number] { 
    width: 10%;
    border: none;
    font-family: 'ABeeZee', sans-serif;
    font-size: 0.5vw;
    color: white;
    background: none;
    -moz-appearance: textfield;
    -webkit-appearance: textfield;
    appearance: textfield;
    text-align: center;
}

.selection_list input[type=range]{
	appearance: none;
	outline: none;
    width: 10vw;
    height: 0.3vw;
	border-radius: 5px;
	background-color: #ccc;
}
.selection_list input[type=range]::-webkit-slider-thumb {
    background: #fafafa;
    appearance: none;
    box-shadow: 1px 2px 26px 1px #bdbdbd;
    width: 0.8vw;
    height: 0.8vw;
    border-radius: 50%;
}

.seperator {
    font-size: 0.5vw;
    margin: 0 0.1vw 0 0.1vw;
    align-self: center;
    justify-content: center;
}

.dcoloumn-window {
    width: 100%;
    height: 100%;
}

.class-section{
    margin-top: 0.5vw;
    height: 1vw;
    width: 100%;
    display: flex;
    font-size: 0.7vw;
    background: #D9D9D9;
}

.class-section img {
    width: 0.7vw;
    position: absolute;
    justify-content: center;
    align-self: center;
    right: 1.1vw;
}

.class-section span {
    width: 100%;
    text-align-last: center;
}

.d-section-slider {
    padding: 4% 5% 0 5%;
}
</style>