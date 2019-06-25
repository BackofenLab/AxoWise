var APP = null;

$(document).ready(function () {
    APP = new Vue({
        el: '#pgdb-app',
        data: {
            gephi_json: null,
            node_color_index: null,
            edge_color_index: null,
            active_node: null,
            active_term: null
        },
        watch: {
            active_node: function(node) {
                var com = this;
                if (node == null) return;

                com.active_term = null;
            },
            active_term: function(term) {
                var com = this;
                if (term == null) return;

                com.active_node = null;
            },
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