var APP = null;

$(document).ready(function () {
    APP = new Vue({
        el: '#pgdb-app',
        data: {
            wait: true,
            last_clicked: null,
            title: "",
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
            threshold: 0.4
        }
    });
});
