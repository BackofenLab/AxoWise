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
        el: '#pgdb-app', // Link to index.html (div in body)
        data: {
            gephi_json: null,
            node_color_index: null,
            edge_color_index: null,
            node2term_index: null,
            active_node: null,
            active_term: null,
            active_subset: null,
            dark_theme_root: true
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

                com.node2term_index = {};
                for (var i in json.enrichment) {
                    var term = json.enrichment[i];
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