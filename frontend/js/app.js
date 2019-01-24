var APP = null;

$(document).ready(function () {
    APP = new Vue({
        el: '#pgdb-app',
        data: {
            api: {
                search: {
                    protein_list: "api/search/protein_list",
                    pathway: "api/search/pathway"
                },
                subgraph: {
                    protein_list: "api/subgraph/protein_list",
                    pathway: "api/subgraph/pathway"
                }
            },
            wait: true,
            last_clicked: null,
            visualization: {
                title: "",
                num_nodes: 0,
                num_edges: 0,
                proteins: true,
                pathways: true,
                classes: true
            },
            rectangular_select: {
                canvas: null,
                context: null,
                rectangle: {},
                active: false,
                surface_backup: null
            },
            species: {
                ncbi_id: null,
                kegg_id: null,
                name: null
            },
            protein: {
                id: null,
                name: null
            },
            pathway: {
                id: null,
                name: null  
            },
            protein_list: {
                value: null,
                ids: []
            },
            threshold: 0.75
        },
        methods: {
            filter_nodes: function(data) {
                if (!data) return;

                var visualization = this.visualization;

                var filtered_nodes = data.nodes.get({
                    filter: function (node) {
                        if (node.color == colors.protein) return visualization.proteins;
                        else if (node.color == colors.pathway) return visualization.pathways;
                        else if (node.color == colors.gray) return visualization.classes;
                        return true;
                    }
                });

                return {
                    nodes: new vis.DataSet(filtered_nodes),
                    edges: data.edges
                };
            },
            threshold_resubmit: function() {
                if(!this.last_clicked) return;
                this.last_clicked.click();
            }
        },
        watch: {
            "visualization.proteins": function (value) {
                visualize_visjs_data(NETWORK_DATA_ALL);
            },
            "visualization.pathways": function (value) {
                visualize_visjs_data(NETWORK_DATA_ALL);
            },
            "visualization.classes": function (value) {
                visualize_visjs_data(NETWORK_DATA_ALL);
            }
        }
    });
});
