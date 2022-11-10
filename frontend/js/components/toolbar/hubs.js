Vue.component("hubs", {
    props: ["gephi_json"],
    data: function() {
        return  {
            message: "",
        }
    },
    methods: {
        get_hubs: function() {
            var com = this;
            let mean = 0;
            const subset = com.gephi_json.nodes.map(arrayItem => {
                return arrayItem.attributes["Degree"]
            });
            // console.log(subset)
            // ---mean calculation---

            // Convert String values to Integers
            var result = subset.map(function (x) { 
                return parseInt(x, 10);
            });
            let sum = result.reduce((accumulator, value) => {
                return accumulator + value;
            });

            mean = sum/subset.length;
            console.log(mean)
            console.log(subset.length)

            // ---empirical standard deviation---

            let stdDev = 0;
            stdDev = Math.sqrt(result.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / (subset.length - 1))
            console.log(stdDev)

            // define threshold

            const treshold = Math.ceil(mean + stdDev)
            console.log(treshold)

            // Filter Hubs

            var nodes = com.gephi_json.nodes;
            i = nodes.length - 1;
            while (i >= 0) {
                if (nodes[i].attributes.Degree >= treshold) {
                    nodes.splice(i, 1);
                }
                i--;
            }

            // console.log(nodes)

            com.$emit("active-subset-changed", nodes);
            /* array.filter(item => item.condition < 10)
            .forEach(item => console.log(item))*/
        },
    },
    template: `
        <div v-show="gephi_json != null" class="toolbar-button">
            <div class="toolbar-theme">
                <button v-on:click="get_hubs()" id="hide_hubs">Hide Hubs</button>
                <span class="toolbar-icon">H</span>
            </div>
        </div>
    `
});