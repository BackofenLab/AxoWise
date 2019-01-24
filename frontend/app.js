var APP = null;

$(document).ready(function () {
    APP = new Vue({
        el: '#pgdb-app',
        data: {
            api: {
                search: {
                    species: "api/search/species",
                    protein: "api/search/protein",
                    protein_list: "api/search/protein_list",
                    pathway: "api/search/pathway"
                },
                subgraph: {
                    protein: "api/subgraph/protein",
                    protein_list: "api/subgraph/protein_list",
                    pathway: "api/subgraph/pathway"
                }
            },
            wait: true,
            visualization: {
                title: "",
                num_nodes: 0,
                num_edges: 0
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
            threshold: {
                min: 0.4,
                max: 1.0,
                step: 0.001,
                value: 0.75
            }
        }
    });
});
