Vue.component("hubs", {
	props: ["gephi_json"],
	data: function() {
		return  {
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
				var subset_degree = com.gephi_json.nodes.map(arrayItem => {
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

			// hide nodes: e.hidden
			// keep the colors

			// filter hubs
			var finalNodes = [];
			var nodes = [];
			// degree filtering
			for (var idx in com.gephi_json.nodes){
				if(parseInt(com.gephi_json.nodes[idx].attributes["Degree"]) >= this.degree_boundary.value){
					nodes.push(com.gephi_json.nodes[idx])
				}
			}
			/*
			// clustering coefficient filterin
			for (var idy in nodes){
				if(parseFloat(nodes[idy].attributes["Clustering Coefficient"]) <= this.cc_boundary.value){
					finalNodes.push(nodes[idy])
				}
			}*/
			finalNodes = nodes;
			com.$emit("active-subset-changed", finalNodes);
			console.log("nodes: ", finalNodes)
		},
	},
	mounted: function() {
		var com = this;

		$("#hubs-slider").slider();
		$("#hubs-slider").change(com.draw_hubs);
		$("#hubs-input").change(com.draw_hubs);

		/*$("#cc-slider").slider();
		$("#cc-slider").change(com.draw_hubs);
		$("#cc-input").change(com.draw_hubs);*/

	},
	template: `
		<div v-show="gephi_json != null" class="toolbar-button">
			<div class="toolbar-theme">
			 <div class="boundary">
				<input id="hubs-slider"
					type="range"
					v-bind:min="degree_boundary.min"
					v-bind:max="degree_boundary.max"
					v-bind:step="degree_boundary.step"
					v-model="degree_boundary.value"
				/>
				<input id="hubs-input"
					type="number"
					v-bind:min="degree_boundary.min"
					v-bind:max="degree_boundary.max"
					v-bind:step="degree_boundary.step"
					v-model="degree_boundary.value"
				/>
			</div>
			<span class="toolbar-icon">H</span>
			<!--<div class="boundary" style="width:20%;">
				<input id="cc-slider"
					type="range"
					v-bind:min="cc_boundary.min"
					v-bind:max="cc_boundary.max"
					v-bind:step="cc_boundary.step"
					v-model="cc_boundary.value"
				/>
				<input id="cc-input"
					type="number"
					v-bind:min="cc_boundary.min"
					v-bind:max="cc_boundary.max"
					v-bind:step="cc_boundary.step"
					v-model="cc_boundary.value"
				/>
			</div>
			<span class="toolbar-icon" style="
			margin-left:10px;">CC</span>-->
			</div>
		</div>
	`
});