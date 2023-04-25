<template>
    <div class="selection_item">
        <span>Betweenness Centrality</span>
        <div class="boundary">
            <input id="bc-slider"
                type="range"
                v-bind:min="bc_boundary.min"
                v-bind:max="bc_boundary.max"
                v-bind:step="bc_boundary.step"
                v-model="bc_boundary.value"
                v-on:change="draw_hubs()"
            />
            <input id="bc-input"
                type="number"
                v-bind:min="bc_boundary.min"
                v-bind:max="bc_boundary.max"
                v-bind:step="bc_boundary.step"
                v-model="bc_boundary.value"
                v-on:change="draw_hubs()"
            />
        </div>
    </div>
</template>

<script>
export default {
    name: 'BetweenesCentrality',
    props: ['gephi_data'],
    data() {
        return {
			once: true,
			bc_boundary: {
				value: 0,
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
				var subset_bc = com.gephi_data.nodes.map(arrayItem => {
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

			// filter
			var nodes = [];
			// degree filtering
			for (var idx in com.gephi_data.nodes){
				if(parseFloat(com.gephi_data.nodes[idx].attributes["Betweenness Centrality"]) >= this.bc_boundary.value){
					nodes.push(com.gephi_data.nodes[idx])
				}
			}
			this.emitter.emit("searchSubset", nodes);
		},
	},
}
</script>

<style>


</style>