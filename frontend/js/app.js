var APP = null;

$(document).ready(function () {
    APP = new Vue({
        el: '#pgdb-app', // Link to index.html (div in body)
        data: {
            gephi_json: null,
            node_color_index: null,
            edge_color_index: null,
            active_node: null,
            active_term: null
        },
        watch: {
            gephi_json: function(json) {
                var com = this;
                com.node_color_index = {};
                for (var idx in json.nodes) {
                    var node = json.nodes[idx];
                    com.node_color_index[node.id] = node.color;
                }

                com.edge_color_index = {};
                for (var idx in json.edges) {
                    var edge = json.edges[idx];
                    com.edge_color_index[edge.id] = edge.color;
                }
            }
        }
    });
});