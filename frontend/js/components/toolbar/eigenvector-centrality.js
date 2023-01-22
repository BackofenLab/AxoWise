Vue.component("eigenvector-centrality", {
	props: ["gephi_json"],
	data: function() {
		return  {
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

			// filter
			var nodes = [];
			// degree filtering
			for (var idx in com.gephi_json.nodes){
				if(parseFloat(com.gephi_json.nodes[idx].attributes["Eigenvector Centrality"]) >= this.ec_boundary.value){
					nodes.push(com.gephi_json.nodes[idx])
				}
			}
			com.$emit("active-subset-changed", nodes);
		},
	},
	mounted: function() {
		var com = this;

		$("#ec-slider").slider();
		$("#ec-slider").change(com.draw_hubs);
		$("#ec-input").change(com.draw_hubs);

	},
	template: `
		<div v-show="gephi_json != null" class="toolbar-button">
			<div class="toolbar-theme">
			 <div class="boundary">
				<input id="ec-slider"
					type="range"
					v-bind:min="ec_boundary.min"
					v-bind:max="ec_boundary.max"
					v-bind:step="ec_boundary.step"
					v-model="ec_boundary.value"
				/>
				<input id="ec-input"
					type="number"
					v-bind:min="ec_boundary.min"
					v-bind:max="ec_boundary.max"
					v-bind:step="ec_boundary.step"
					v-model="ec_boundary.value"
				/>
			</div>
			<span class="toolbar-icon">EC</span>
			</div>
		</div>
	`
});