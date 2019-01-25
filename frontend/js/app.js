var APP = null;

$(document).ready(function () {
    APP = new Vue({
        el: '#pgdb-app',
        data: {
            wait: true,
            last_clicked: null,
            title: "",
            rectangular_select: {
                canvas: null,
                context: null,
                rectangle: {},
                active: false,
                surface_backup: null
            },
            data: {
                nodes: new vis.DataSet(),
                edges: new vis.DataSet(),
            },
            show: {
                proteins: true,
                pathways: true,
                classes: true
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
            protein_list: null,
            threshold: 0.75
        },
        methods: {
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
