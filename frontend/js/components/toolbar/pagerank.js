Vue.component("pagerank", {
	props: ["gephi_json"],
	data: function() {
		return  {
			once: true,
			pr_boundary: {
				value: 0.01,
				min: 0,
				max: 0.1,
				step: 0.01
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
				if(parseFloat(com.gephi_json.nodes[idx].attributes["PageRank"]) >= this.pr_boundary.value){
					nodes.push(com.gephi_json.nodes[idx])
				}
			}
			com.$emit("active-subset-changed", nodes);
		},
	},
	mounted: function() {
		var com = this;

		$("#pr-slider").slider();
		$("#pr-slider").change(com.draw_hubs);
		$("#pr-input").change(com.draw_hubs);

	},
	template: `
		<div v-show="gephi_json != null" class="toolbar-button">
			<div class="toolbar-theme">
			 <div class="boundary">
				<input id="pr-slider"
					type="range"
					v-bind:min="pr_boundary.min"
					v-bind:max="pr_boundary.max"
					v-bind:step="pr_boundary.step"
					v-model="pr_boundary.value"
				/>
				<input id="pr-input"
					type="number"
					v-bind:min="pr_boundary.min"
					v-bind:max="pr_boundary.max"
					v-bind:step="pr_boundary.step"
					v-model="pr_boundary.value"
				/>
			</div>
			<span class="toolbar-icon">PR</span>
			</div>
		</div>
	`
});