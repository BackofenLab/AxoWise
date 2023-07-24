<template>
    <div class="selection_item">
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
</template>

<script>
export default {
    name: 'PadjSelection',
    props: ['term_data'],
    data() {
        return {
            once: true,
			padj_boundary: {
				value: 0,
				min: 0,
				max: 1000,
				step: 1
			},
        }
    },
    methods: {
		draw_padj: function() {
			var com = this;
			// initialize values of slider
			

			// filter hubs
			var finalNodes = [];
			// degree filtering
			for (var idx in com.term_data.nodes){
                if(Math.abs(Math.log(com.term_data.nodes[idx].attributes["FDR"])) >= com.padj_boundary.value) finalNodes.push(com.term_data.nodes[idx]) 
			}
            this.emitter.emit("searchTermSubset", finalNodes);
		},
	},
}
</script>

<style>
</style>