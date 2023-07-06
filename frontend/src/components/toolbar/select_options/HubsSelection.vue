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
    </div>
</template>

<script>
export default {
    name: 'HubsSelection',
    props: ['gephi_data','term_data'],
    data() {
        return {
            once: true,
			cc_boundary: {
				value: 0.2,
				min: 0,
				max: 1.0,
				step: 0.1
			},
			degree_boundary: {
				value: Number,
				min: 0,
				max: Number,
				step: 1
			},
        }
    },
    methods: {
		draw_hubs: function() {
			var com = this;

			var dataForm = com.gephi_data || com.term_data;
            var searchSubset = (dataForm === com.gephi_data) ? "searchSubset" : "searchTermSubset";

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

			// filter hubs
			var finalNodes = [];
			var nodes = [];
			// degree filtering
			for (var idz in dataForm.nodes){
				if(parseInt(dataForm.nodes[idz].attributes["Degree"]) >= this.degree_boundary.value){
					nodes.push(dataForm.nodes[idz])
				}
			}
			finalNodes = nodes;
			this.emitter.emit(searchSubset, finalNodes);
		},
	},
}
</script>

<style>
</style>