var APP = null;
const eventHub = new Vue(); // Single event hub

 // Distribute to components using global mixin
 Vue.mixin({
     data: function () {
         return {
             eventHub: eventHub
         }
     }
 })

$(document).ready(function () {
    APP = new Vue({
        el: '#webapp', // Link to index.html (div in body)
        data: {
            gephi_json: null,
            node_color_index: null,
            edge_color_index: null,
            node2term_index: null,
            active_node: null,
            active_term: null,
            active_subset: null,
            active_layer: null,
            dark_theme_root: true,
            d_value: null,
            func_json: null,
            func_enrichment: null,
            revert_term: null,
            reset_term: null,
            home_button: null,
            snapshot: null,
            protein_list: null,
            hubs: null,
            unconnected_graph: null,
        },
        watch: {
            gephi_json: function(json) {
                if (!json) return ; //handling null json from backend
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
            },
            func_enrichment: function(enrichment) {
                if (!enrichment) return ; //handling null json from backend
                var com = this;
                com.node2term_index = {};               
                for (var i in enrichment) {
                    var term = enrichment[i];
                    for (var j in term.proteins) {
                        var ensembl_id = term.proteins[j];
                        if (!(ensembl_id in com.node2term_index)) com.node2term_index[ensembl_id] = new Set();
                        com.node2term_index[ensembl_id].add(term);
                    }
                }
            }
        }
    });
});