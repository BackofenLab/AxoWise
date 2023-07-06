<template>
    <div class="selection_item">
        <span>Eigenvector</span>
        <div class="boundary">
            <input id="ec-slider"
                type="range"
                v-bind:min="ec_boundary.min"
                v-bind:max="ec_boundary.max"
                v-bind:step="ec_boundary.step"
                v-model="ec_boundary.value"
                v-on:change="draw_hubs()"
            />
            <input id="ec-input"
                type="number"
                v-bind:min="ec_boundary.min"
                v-bind:max="ec_boundary.max"
                v-bind:step="ec_boundary.step"
                v-model="ec_boundary.value"
                v-on:change="draw_hubs()"
            />
        </div>
    </div>
</template>

<script>
export default {
    name: 'EigenvectorCentrality',
    props: ['gephi_data','term_data'],
    data() {
        return {
            ec_boundary: {
                value: 0.2,
                min: 0,
                max: 1,
                step: 0.1
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
				if(parseFloat(dataForm.nodes[idz].attributes["Eigenvector Centrality"]) >= this.ec_boundary.value){
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