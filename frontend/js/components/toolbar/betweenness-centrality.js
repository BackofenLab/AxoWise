Vue.component("betweenness-centrality", {
	props: ["gephi_json"],
	data: function() {
		return  {
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
			console.log("com: ", com)
			// initialize values of slider
			if (com.once) {
				// _____ this calculation has only to be done once _______
				var subset_bc = com.gephi_json.nodes.map(arrayItem => {
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
			for (var idx in com.gephi_json.nodes){
				if(parseFloat(com.gephi_json.nodes[idx].attributes["Betweenness Centrality"]) >= this.bc_boundary.value){
					nodes.push(com.gephi_json.nodes[idx])
				}
			}
			com.$emit("active-subset-changed", nodes);
		},
	},
	mounted: function() {
		var com = this;

		$("#bc-slider").slider();
		$("#bc-slider").change(com.draw_hubs);
		$("#bc-input").change(com.draw_hubs);

	},
	template: `
		<div v-show="gephi_json != null" class="toolbar-button">
			<div class="toolbar-theme">
			 <div class="boundary">
				<input id="bc-slider"
					type="range"
					v-bind:min="bc_boundary.min"
					v-bind:max="bc_boundary.max"
					v-bind:step="bc_boundary.step"
					v-model="bc_boundary.value"
				/>
				<input id="bc-input"
					type="number"
					v-bind:min="bc_boundary.min"
					v-bind:max="bc_boundary.max"
					v-bind:step="bc_boundary.step"
					v-model="bc_boundary.value"
				/>
			</div>
			<span class="toolbar-icon">BC</span>
			</div>
		</div>
	`
});