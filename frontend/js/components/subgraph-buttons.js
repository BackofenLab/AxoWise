Vue.component("subgraph-buttons", {
    props: ["data_node"],
    methods: {
        // reduce graph button
        reduce: function() {
            var com = this;
            if (!NETWORK || !com.data_node) return;

            var data = com.data_node.data;
            var selected = NETWORK.getSelection();
            if (selected.nodes.length <=0) return;

            var nodes_protein = data.nodes_protein.get({
                filter: function (node) {
                    return (selected.nodes.indexOf(node.id) >= 0);
                }
            });

            var edges = data.edges.get({
                filter: function (edge) {
                    return (selected.edges.indexOf(edge.id) >= 0) || edge.color == colors.pathway;
                }
            });

            var data = {
                nodes_protein: new vis.DataSet(nodes_protein),
                nodes_pathway: data.nodes_pathway,
                nodes_class: data.nodes_class,
                edges: new vis.DataSet(edges)
            };

            com.$emit("data-child-created", {
                name: com.data_node.name,
                data: data,
                index: com.data_node.index.slice(),
                children: []
            });
        },
        stabilize: function() {
            if (!NETWORK) return;
            NETWORK.stabilize(50);
        }
    },
    template: `
        <div class="col-md-4 ui-widget">
            <button id="reduce-graph-btn"
                    class="btn btn-danger"
                    v-bind:disabled="$root.wait"
                    v-on:click="reduce()"
            ><span class="glyphicon glyphicon-scissors"></span> Reduce</button>
            <button id="reduce-graph-btn"
                    class="btn btn-success"
                    v-bind:disabled="$root.wait"
                    v-on:click="stabilize()"
            ><span class="glyphicon glyphicon-refresh"></span> Stabilize</button>
        </div>
    `
});