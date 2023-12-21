<template>
        <div class="tool-item">
        <div id="selection_highlight" class="window-menu">
            <div class="selection_list">
                <div class="window-label">degree value</div>
                <div class="menu-items">
                    <input
                        id="degree"
                        type="range"
                        v-bind:min="degree_boundary.min" v-bind:max="degree_boundary.max" v-bind:step="degree_boundary.step"
                        v-model="degree_boundary.value"
                        v-on:change="searchSubset()"
                        v-on:input="valueChanged('degree')"
                    />
                    <input
                        type="number"
                        v-bind:min="degree_boundary.min" v-bind:max="degree_boundary.max" v-bind:step="degree_boundary.step"
                        v-model="degree_boundary.value"
                        v-on:change="searchSubset()"
                        v-on:input="valueChanged('degree')"
                    />
                </div>
                <div class="window-label">betweenness centrality value</div>
                <div class="menu-items">
                    <input
                        id="bcentrality"
                        type="range"
                        v-bind:min="bc_boundary.min" v-bind:max="bc_boundary.max" v-bind:step="bc_boundary.step"
                        v-model="bc_boundary.value"
                        v-on:change="searchSubset()"
                        v-on:input="valueChanged('bcentrality')"
                    />
                    <input
                        type="number"
                        v-bind:min="bc_boundary.min" v-bind:max="bc_boundary.max" v-bind:step="bc_boundary.step"
                        v-model="bc_boundary.value"
                        v-on:change="searchSubset()"
                        v-on:input="valueChanged('bcentrality')"
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
                        <input 
                            type="number"
                            v-bind:min="padj_boundary.min" v-bind:max="padj_boundary.max" v-bind:step="padj_boundary.step"
                            v-model="padj_boundary.value"
                            v-on:change="searchSubset()"
                            v-on:input="valueChanged('padj')"
                        />
                    </div>
                </div>
                <div class="window-label">page rank value</div>
                <div class="menu-items">
                    <input
                        id="pagerank"
                        type="range"
                        v-bind:min="pr_boundary.min" v-bind:max="pr_boundary.max" v-bind:step="pr_boundary.step"
                        v-model="pr_boundary.value"
                        v-on:change="searchSubset()"
                        v-on:input="valueChanged('pagerank')"
                    />
                    <input 
                        type="number"
                        v-bind:min="pr_boundary.min" v-bind:max="pr_boundary.max" v-bind:step="pr_boundary.step"
                        v-model="pr_boundary.value"
                        v-on:change="searchSubset()"
                        v-on:input="valueChanged('pagerank')"
                    />
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
export default {
    name: 'SelectionList',
    props: ['data','mode','active_subset', 'active_term'],
    emits: ['selection_active_changed'],
    data() {
        return {
            once: true,
            search_data: null,
			degree_boundary: {
				value: 0,
				min: 0,
				max: Number,
				step: 1
			},
            pr_boundary: {
                value: 0,
				min: 0,
				max: Number,
				step: 0.0001
            },
            bc_boundary: {
				value: 0,
				min: 0,
				max: Number,
				step: 1
			},
            padj_boundary: {
				value: 0,
				min: 0,
				max: 1000,
				step: 1
			},
        }
    },
    watch: {
        active_subset(){
            if(!this.active_subset.selection) this.unactive_proteinlist()
        },
        active_term(){
            this.unactive_proteinlist()
        }
    },
    methods: {
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
            // let mean = 0;
            var subset_degree;

            subset_degree = dataForm.nodes.map(arrayItem => {
                return arrayItem.attributes["Degree"]
            });

            // ---mean calculation---

            // Convert String values to Integers
            var result = subset_degree.map(function (x) { 
                return parseInt(x, 10);
            });

            // let sum = result.reduce((accumulator, value) => {
            //     return accumulator + value;
            // });

            // mean = sum/subset_degree.length;

            // ---empirical standard deviation---

            // let stdDev = 0;
            // stdDev = Math.sqrt(result.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / (subset_degree.length - 1));

            // set init degree and max value
            // var init_degree = Math.ceil(mean + (2*stdDev));
            var maxDeg = Math.max(...result);       // Need to use spread operator!

            // this.degree_boundary.value = init_degree;
            this.degree_boundary.max = maxDeg;
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
                return parseInt(x, 10);
            });
            var maxDeg = Math.max(...result);       // Need to use spread operator!

            this.bc_boundary.max = maxDeg;

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
            var maxDeg = Math.max(...result);       // Need to use spread operator!

            this.pr_boundary.max = maxDeg;

        },
        searchSubset() {
            var com = this

            var dataForm = com.search_data;
            console.log(dataForm)
            // filter hubs
			var finalNodes = [];
			var nodes = [];
			// degree filtering
			for (var element of dataForm){
				if(parseInt(element.attributes["Degree"]) >= this.degree_boundary.value &&
                   parseFloat(element.attributes["PageRank"]) >= this.pr_boundary.value &&
                   parseFloat(element.attributes["Betweenness Centrality"]) >= this.bc_boundary.value
                   ){
                    if(com.mode=='term'){
                        if(Math.abs(Math.log10(element.attributes["FDR"])) >= com.padj_boundary.value) nodes.push(element)
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
            this.emitter.emit("searchSubset", {subset:this.search_data, mode:this.mode});
        },
        valueChanged(id){
            var target = document.getElementById(id)
            let a = (target.value / target.max)* 100;
            target.style.background = `linear-gradient(to right,#0A0A1A,#0A0A1A ${a}%,#ccc ${a}%)`;
        },
        term_genes(list){
            var term_genes = new Set(list)
            var termlist = this.data.nodes.filter(element => term_genes.has(element.attributes["Name"]))
            return termlist
        }
	},
    mounted(){
        this.search_data = this.active_term ? this.term_genes(this.active_term.symbols) : (this.active_subset ? this.active_subset : this.data.nodes);
        this.dragElement(document.getElementById("selection_highlight"));
        
    },
    created() {
        this.initialize_dg()
        this.initialize_bc()
        this.initialize_pagerank()
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
}

.selection_list .window-label {
    color: white;
}

.selection_list input[type=number] { 
    position: absolute;
    margin-top:0.2vw;
    right: 5%;
    width: 20%;
    border: none;
    height: 6%;
    font-family: 'ABeeZee', sans-serif;
    font-size: 0.7vw;
    color:  white;
    background: none;
    -moz-appearance: textfield;
    appearance: textfield;
    text-align: right;
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

</style>