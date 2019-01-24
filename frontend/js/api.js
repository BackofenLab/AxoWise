
$(document).ready(function () {
    var progressbar = $("#progressbar");

    // --------------- Protein list ---------------
    $("#protein-list-btn").click(() => {
        if (!APP.species.ncbi_id) {
            alert("Select the species first!")
            return;
        }

        // Vue.js
        APP.visualization.title = "";

        // wait
        progressbar.progressbar("option", "value", false);

        $.get(APP.api.search.protein_list, { query: APP.protein_list.value.split('\n').join(';'), species_id: APP.species.ncbi_id })
                .done(function (data) {
                    APP.protein_list.ids = data.map(x => x.protein_id);

                    var threshold = parseFloat(APP.threshold.value);
                    $.get(APP.api.subgraph.protein_list, { protein_ids: APP.protein_list.ids.join(';'), threshold: threshold })
                        .done(function (subgraph) {
                            var data = protein_list_subgraph_to_visjs_data(subgraph);
                            NETWORK_DATA_ALL = data;
                            visualize_visjs_data(data);

                            // Vue.js
                            APP.last_clicked = $("#protein-list-btn");

                            // wait is over
                            progressbar.progressbar("option", "value", 0);
                            APP.wait = false;
                        });
                });
    });

});