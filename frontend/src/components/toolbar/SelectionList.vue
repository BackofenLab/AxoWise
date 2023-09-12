<template>
    <div class="selection_item">
        <span>Hubs</span>
        <div class="boundary">
            <input id="hubs-slider"
                type="range"
                v-bind:min="degree_boundary.min"
                v-bind:max="degree_boundary.max"
                v-bind:step="degree_boundary.step"
                v-model="degree_boundary.value"
                v-on:change="draw_hubs()"
            />
            <input id="hubs-input"
                type="number"
                v-bind:min="degree_boundary.min"
                v-bind:max="degree_boundary.max"
                v-bind:step="degree_boundary.step"
                v-model="degree_boundary.value"
                v-on:change="draw_hubs()"
            />
        </div>
        <span>Betweenness Centrality</span>
        <div class="boundary">
            <input id="bc-slider"
                type="range"
                v-bind:min="bc_boundary.min"
                v-bind:max="bc_boundary.max"
                v-bind:step="bc_boundary.step"
                v-model="bc_boundary.value"
                v-on:change="draw_bc()"
            />
            <input id="bc-input"
                type="number"
                v-bind:min="bc_boundary.min"
                v-bind:max="bc_boundary.max"
                v-bind:step="bc_boundary.step"
                v-model="bc_boundary.value"
                v-on:change="draw_bc()"
            />
        </div>
        <span>PageRank</span>
        <div class="boundary">
            <input id="pr-slider"
                type="range"
                v-bind:min="pr_boundary.min"
                v-bind:max="pr_boundary.max"
                v-bind:step="pr_boundary.step"
                v-model="pr_boundary.value"
                v-on:change="draw_hubs()"
            />
            <input id="pr-input"
                type="number"
                v-bind:min="pr_boundary.min"
                v-bind:max="pr_boundary.max"
                v-bind:step="pr_boundary.step"
                v-model="pr_boundary.value"
                v-on:change="draw_hubs()"
            />
        </div>
        <div v-show="term_data">
            <span>Padj</span>
            <div class="boundary">
                <input id="padj-slider"
                type="range"
                v-bind:min="padj_boundary.min"
                v-bind:max="padj_boundary.max"
                v-bind:step="padj_boundary.step"
                v-model="padj_boundary.value"
                v-on:change="draw_padj()"
                />
                <input id="padj-input"
                type="number"
                v-bind:min="padj_boundary.min"
                v-bind:max="padj_boundary.max"
                v-bind:step="padj_boundary.step"
                v-model="padj_boundary.value"
                v-on:change="draw_padj()"
                />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'SelectionList',
    props: ['gephi_data','term_data'],
    data() {
        return {
            once: true,
			cc_boundary: {
				value: 0,
				min: 0,
				max: 1.0,
				step: 0.01
			},
			degree_boundary: {
				value: Number,
				min: 0,
				max: Number,
				step: 1
			},
            pr_boundary: {
                value: 0.0001,
				min: 0,
				max: 0.02,
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
    methods: {
		draw_hubs: function() {
			var com = this;

            console.log(com.term_data)

			var dataForm = com.gephi_data || com.term_data;

			// initialize values of slider
			if (com.once) {
				// _____ this calculation has only to be done once _______
				let mean = 0;
				var subset_degree;

				subset_degree = dataForm.nodes.map(arrayItem => {
					return arrayItem.attributes["Degree"]
				});

				// ---mean calculation---

				// Convert String values to Integers
				var result = subset_degree.map(function (x) { 
					return parseInt(x, 10);
				});

				let sum = result.reduce((accumulator, value) => {
					return accumulator + value;
				});

				mean = sum/subset_degree.length;

				// ---empirical standard deviation---

				let stdDev = 0;
				stdDev = Math.sqrt(result.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / (subset_degree.length - 1));

				// set init degree and max value
				var init_degree = Math.ceil(mean + (2*stdDev));
				var maxDeg = Math.max(...result);       // Need to use spread operator!

				this.degree_boundary.value = init_degree;
				this.degree_boundary.max = maxDeg;
				com.once = false;

			}
            this.searchSubset(dataForm)
		},
        draw_bc: function() {
            var com = this;

			var dataForm = com.gephi_data || com.term_data;

			// initialize values of slider
			if (com.once) {
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
				com.once = false;
			}
            
            this.searchSubset(dataForm)
        },
        draw_pr: function(){
            var com = this
            var dataForm = com.gephi_data || com.term_data;

            this.searchSubset(dataForm)

        },
        draw_padj: function(){
            var com = this
            var dataForm = com.gephi_data || com.term_data;

            this.searchSubset(dataForm)

        },

        searchSubset(dataForm) {
            var com = this
            var searchSubset = (dataForm === com.gephi_data) ? "searchSubset" : "searchTermSubset";
            // filter hubs
			var finalNodes = [];
			var nodes = [];
			// degree filtering
			for (var idz in dataForm.nodes){
				if(parseInt(dataForm.nodes[idz].attributes["Degree"]) >= this.degree_boundary.value &&
                   parseFloat(dataForm.nodes[idz].attributes["PageRank"]) >= this.pr_boundary.value &&
                   parseFloat(dataForm.nodes[idz].attributes["Betweenness Centrality"]) >= this.bc_boundary.value
                   ){
                    if(com.term_data){
                        if(Math.abs(Math.log10(dataForm.nodes[idz].attributes["FDR"])) >= com.padj_boundary.value) nodes.push(dataForm.nodes[idz])
                    }
                    else{
                        nodes.push(dataForm.nodes[idz])
                    }
				}
			}
			finalNodes = nodes;
			this.emitter.emit(searchSubset, finalNodes);
        }
	},
}
</script>

<style>
</style>