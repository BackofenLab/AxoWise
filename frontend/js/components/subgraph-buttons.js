Vue.component("subgraph-buttons", {
    props: ["data_node"],
    methods: {
        // reduce graph button
        reduce: function() {
            var com = this;
            if (!NETWORK || !com.data_node) return;

            var data = com.data_node.data;
            var selected = NETWORK.getSelection();

            var nodes = data.nodes.get({
                filter: function (node) {
                    return (selected.nodes.indexOf(node.id) >= 0);
                }
            });

            var edges = data.edges.get({
                filter: function (edge) {
                    return (selected.edges.indexOf(edge.id) >= 0);
                }
            });

            var data = {
                nodes: new vis.DataSet(nodes),
                edges: new vis.DataSet(edges)
            };

            com.$emit("data-child-created", {
                name: "dummy",
                data: data,
                children: []
            });
        }
    },
    template: `
        <div class="col-md-4 ui-widget">
            <button id="reduce-graph-btn"
                    class="btn btn-warning"
                    v-bind:disabled="$root.wait"
                    v-on:click="reduce()"
            ><span class="glyphicon glyphicon-scissors"></span> Reduce</button>
        </div>
    `
});