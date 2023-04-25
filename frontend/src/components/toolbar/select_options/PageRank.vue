<template>
    <div class="selection_item">
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
    </div>
</template>

<script>

export default {
    name: 'PageRank',
    props: ['gephi_data'],
    data() {
        return {
			once: true,
			pr_boundary: {
				value: 0.0001,
				min: 0,
				max: 0.02,
				step: 0.0001
			},
        }
    },
    methods: {
		draw_hubs: function() {
			var com = this;


			// filter
			var nodes = [];
			// degree filtering
			for (var idx in com.gephi_data.nodes){
				if(parseFloat(com.gephi_data.nodes[idx].attributes["PageRank"]) >= this.pr_boundary.value){
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