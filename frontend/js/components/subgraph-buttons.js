Vue.component("subgraph-buttons", {
    props: ["data"],
    methods: {
        // reduce graph button
        reduce: function() {
            var com = this;
            if (!NETWORK) return;

            var selected = NETWORK.getSelection();

            var nodes = com.data.nodes.get({
                filter: function (node) {
                    return (selected.nodes.indexOf(node.id) >= 0);
                }
            });

            var edges = com.data.edges.get({
                filter: function (edge) {
                    return (selected.edges.indexOf(edge.id) >= 0);
                }
            });

            com.$emit("data-changed", {
                nodes: new vis.DataSet(nodes),
                edges: new vis.DataSet(edges)
            });
        }
    },
    template: `
        <div class="col-md-4 ui-widget">
            <button id="reduce-graph-btn"
                    class="btn btn-warning"
                    v-bind:disabled="$root.wait"
                    v-on:click="reduce()"
            >Reduce</button>
        </div>
    `
});