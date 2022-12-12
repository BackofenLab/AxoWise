Vue.component("hubs", {
    props: ["gephi_json"],
    data: function() {
        return  {
            edge_thick: {
                value: 0.2,
                min: 0,
                max: 1.0,
                step: 0.1
            },
        }
    },
    methods: {
        draw_hubs: function() {
            var com = this;
            let mean = 0;
            var subset = com.gephi_json.nodes.map(arrayItem => {
                return arrayItem.attributes["Degree"]
            });

            // ---mean calculation---

            // Convert String values to Integers
            var result = subset.map(function (x) { 
                return parseInt(x, 10);
            });
            let sum = result.reduce((accumulator, value) => {
                return accumulator + value;
            });

            mean = sum/subset.length;

            // ---empirical standard deviation---

            let stdDev = 0;
            stdDev = Math.sqrt(result.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / (subset.length - 1))

            // define threshold

            const treshold = Math.ceil(mean + (2*stdDev))

            console.log(treshold)

            // filter hubs
            var nodes = [];
            for (var idx in com.gephi_json.nodes){
                if(com.gephi_json.nodes[idx].attributes["Degree"] < treshold && state == "Hide Hubs"){
                    nodes.push(com.gephi_json.nodes[idx])
                }
                if(com.gephi_json.nodes[idx].attributes["Degree"] >= treshold && state == "Show Hubs"){
                    nodes.push(com.gephi_json.nodes[idx])
                }
            
            com.$emit("unconnected-graph-changed", [com.gephi_json.subgraph, state]);
            com.$emit("active-subset-changed", nodes);
            /* array.filter(item => item.condition < 10)
            .forEach(item => console.log(item))*/
            }
            console.log("Start");
        },
    },
    mounted: function() {
        var com = this;

        $("#hubs-slider").slider();
        $("#hubs-slider").change(com.draw_hubs);
        $("#hubs-input").change(com.draw_hubs);

    },
    template: `
        <div v-show="gephi_json != null" class="toolbar-button">
            <div class="toolbar-theme">
             <div class="boundary">
                <input id="hubs-slider"
                    type="range"
                    v-bind:min="edge_thick.min"
                    v-bind:max="edge_thick.max"
                    v-bind:step="edge_thick.step"
                    v-model="edge_thick.value"
                />
                <input id="hubs-input"
                    type="number"
                    v-bind:min="edge_thick.min"
                    v-bind:max="edge_thick.max"
                    v-bind:step="edge_thick.step"
                    v-model="edge_thick.value"
                />
            </div>
            <span class="toolbar-icon">H</span>
            </div>
        </div>
    `
});