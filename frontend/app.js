var APP = null;

$(document).ready(function () {
    APP = new Vue({
        el: '#pgdb-app',
        data: {
            title: null,
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
