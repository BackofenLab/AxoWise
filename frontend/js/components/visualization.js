var NETWORK = null;
var NETWORK_DATA_ALL = null;
var NETWORK_DATA_CURRENT = null;

Vue.component("visualization", {
    props: ["data", "show", "title"],
    data: function() {
        return {
            stats: {
                nodes: 0,
                edges: 0,
            }
        }
    },
    computed: {
        filtered_data: function() {
            var com = this;

            if (!com.data) return;

            var filtered_nodes = com.data.nodes.get({
                filter: function (node) {
                    if (node.color == colors.protein) return com.show.proteins;
                    else if (node.color == colors.pathway) return com.show.pathways;
                    else if (node.color == colors.gray) return com.show.classes;
                    return true;
                }
            });

            return {
                nodes: new vis.DataSet(filtered_nodes),
                edges: com.data.edges
            };
        }
    },
    methods: {
        draw: function(data) {
            if (!NETWORK) return;
            var com = this;

            NETWORK_DATA_CURRENT = data;
        
            NETWORK.setData(data);
            NETWORK.stabilize(50);
        
            // Vis.js
            this.stats.nodes = data.nodes.length;
            this.stats.edges = data.edges.length;
        
            if (data.selected_nodes)
                NETWORK.selectNodes(data.selected_nodes);
        }
    },
    watch: {
        "filtered_data": function(data) {
            var com = this;
            com.draw(data);
        }
    },
    template: `
        <div>
        <div id="visualization" class="col-md-12"></div>
        <div id="info" class="col-md-4">
            {{title}}<br/>
            Nodes: {{stats.nodes}}<br/>
            Edges: {{stats.edges}}<br/>
        </div>
        </div>
    `
});