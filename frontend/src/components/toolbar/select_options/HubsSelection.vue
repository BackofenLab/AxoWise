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
    props: ['gephi_data'],
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
			// initialize values of slider
			if (com.once) {
				// _____ this calculation has only to be done once _______
				let mean = 0;
				var subset_degree = com.gephi_data.nodes.map(arrayItem => {
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
			for (var idx in com.gephi_data.nodes){
				if(parseInt(com.gephi_data.nodes[idx].attributes["Degree"]) >= this.degree_boundary.value){
					nodes.push(com.gephi_data.nodes[idx])
				}
			}
			finalNodes = nodes;
            this.emitter.emit("searchSubset", finalNodes);
		},
	},
}
</script>

<style>
    .boundary {
        border-radius: 20px;
        background: white;
        padding: 10px;
        margin: 10px;
    }

</style>