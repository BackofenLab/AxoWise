
$(document).ready(function () {
    var species = $("#species");
    var protein = $("#protein"); protein.prop("disabled", true);
    var protein_btn = $("#protein-btn"); protein_btn.prop("disabled", true);
    var pathway = $("#pathway"); pathway.prop("disabled", true);
    var pathway_btn = $("#pathway-btn"); pathway_btn.prop("disabled", true);
    var protein_list = $("#protein-list"); protein_list.prop("disabled", true);
    var protein_list_btn = $("#protein-list-btn"); protein_list_btn.prop("disabled", true);

    // --------------- Species ---------------
    var suggested_species_list = {};
    var selected_species = null;

    species.autocomplete({
        source: (request, response) => {
            $.get("api/search/species", { query: species.val() })
                .done(function (data) {
                    data.forEach((e) => {
                        suggested_species_list[e.species_name] = {ncbi_id: e.ncbi_id, kegg_id: e.kegg_id};
                    });
                    response(data.map(x => x.species_name));
                });
        },
        select: (event, ui) => {
            species_name = ui["item"]["value"];
            selected_species = suggested_species_list[species_name];
            protein.prop("disabled", false); protein_btn.prop("disabled", false);
            pathway.prop("disabled", false); pathway_btn.prop("disabled", false);
            protein_list.prop("disabled", false); protein_list_btn.prop("disabled", false);
        }
    });

    // --------------- Protein ---------------
    var suggested_protein_list = {};
    var selected_protein = null;

    protein.autocomplete({
        source: (request, response) => {
            if (selected_species == null) {
                alert("Select the species first!")
                return;
            }

            $.get("api/search/protein", { query: protein.val(), species_id: selected_species["ncbi_id"] })
                .done(function (data) {
                    data.forEach((e) => {
                        suggested_protein_list[e.protein_name] = {protein_id: e.protein_id};
                    });
                    response(data.map(x => x.protein_name));
                });
        },
        select: (event, ui) => {
            protein_name = ui["item"]["value"];
            selected_protein = suggested_protein_list[protein_name];
        }
    });

    protein_btn.click(() => {
        var threshold = parseFloat($("#threshold-value").text());
        $.get("api/subgraph/protein", { protein_id: selected_protein.protein_id, threshold: threshold })
            .done(function (subgraph) {
                $("#data").text(JSON.stringify(subgraph, null, '\t'));
                data = protein_subgraph_to_visjs_data(subgraph);
                visualize_visjs_data(data, false);
            });
    });

    // --------------- Pathway ---------------
    var suggested_pathway_list = {};
    var selected_pathway = null;

    pathway.autocomplete({
        source: (request, response) => {
            if (selected_species == null) {
                alert("Select the species first!")
                return;
            }

            $.get("api/search/pathway", { query: pathway.val(), species_id: selected_species["ncbi_id"] })
                .done(function (data) {
                    data.forEach((e) => {
                        suggested_pathway_list[e.pathway_name] = {pathway_id: e.pathway_id};
                    });
                    response(data.map(x => x.pathway_name));
                });
        },
        select: (event, ui) => {
            pathway_name = ui["item"]["value"];
            selected_pathway = suggested_pathway_list[pathway_name];
        }
    });

    pathway_btn.click(() => {
        $.get("api/subgraph/pathway", { pathway_id: selected_pathway.pathway_id })
            .done(function (subgraph) {
                $("#data").text(JSON.stringify(subgraph, null, '\t'));
                data = pathway_subgraph_to_visjs_data(subgraph);
                visualize_visjs_data(data, false);
            });
    });

    // --------------- Protein list ---------------
    protein_list.autocomplete({
        source: (request, response) => {



        },
        select: (event, ui) => {
            protein_name = ui["item"]["value"];
            selected_protein = protein_list[protein_name];
        }
    });

    protein_list_btn.click(() => {
        if (selected_species == null) {
            alert("Select the species first!")
            return;
        }

        $.get("api/search/protein_list", { query: protein_list.val().split('\n').join(';'), species_id: selected_species["ncbi_id"] })
                .done(function (data) {
                    var protein_ids = data.map(x => x.protein_id);

                    var threshold = parseFloat($("#threshold-value").text());
                    $.get("api/subgraph/protein_list", { protein_ids: protein_ids.join(';'), threshold: threshold })
                        .done(function (subgraph) {
                            $("#data").text(JSON.stringify(subgraph, null, '\t'));
                            data = protein_list_subgraph_to_visjs_data(subgraph);
                            visualize_visjs_data(data, false);
                        });
                });
    });

});