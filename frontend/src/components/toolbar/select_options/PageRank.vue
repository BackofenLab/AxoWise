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
    props: ['gephi_data','term_data'],
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
            
            var dataForm = com.gephi_data || com.term_data;
            var searchSubset = (dataForm === com.gephi_data) ? "searchSubset" : "searchTermSubset";

			// filter
			var nodes = [];
			// degree filtering
                for (var idz in dataForm.nodes){
                    if(parseFloat(dataForm.nodes[idz].attributes["PageRank"]) >= this.pr_boundary.value){
                        nodes.push(dataForm.nodes[idz])
                    }
                }
                this.emitter.emit(searchSubset, nodes);
		},
	},
}
</script>

<style>
</style>