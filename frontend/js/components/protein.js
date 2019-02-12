Vue.component("protein", {
    model: {
        prop: "protein",
        event: "protein-selected"
    },
    props: ["protein", "species", "threshold"],
    data: function() {
        return {
            api: {
                search: "api/search/protein",
                subgraph: "api/subgraph/protein"
            },
            suggested_protein_list: {}
        }
    },
    methods: {
        subgraph_to_visjs_data: function(subgraph) {
            var nodes = new vis.DataSet();
            var edges = new vis.DataSet();
            var selected_nodes = [];
            if (!subgraph)
                return {
                    nodes: nodes,
                    edges: edges,
                    selected_nodes: selected_nodes
                }

            var protein = subgraph.protein;
            var pathways = subgraph.pathways;
            var associations = subgraph.associations;

            // Queried protein
            nodes.update({
                id: protein.id,
                label: protein.name,
                title: get_tooltip(protein.id, protein.description),
                color: {
                    background: colors.protein,
                    border: colors.protein,
                    highlight: "#FFFF00"
                }
            });
            selected_nodes.push(protein.id);

            // Its associated pathways
            for (var i = 0; i < pathways.length; i++) {
                var pathway = pathways[i];

                nodes.update({
                    id: pathway.id,
                    label: pathway.name,
                    title: get_tooltip(pathway.id, pathway.description),
                    color: {
                        background: colors.pathway,
                        border: colors.pathway,
                        highlight: "#FFFF00"
                    },
                    shape: "square"
                });

                edges.update([
                    {
                        from: protein.id,
                        to: pathway.id,
                        color: colors.pathway
                    }
                ]);
            }

            // Interactions with other proteins
            for (var i = 0; i < associations.length; i++) {
                var association = associations[i];
                var other = association.other;
                var combined_score = association.combined_score;

                nodes.update({
                    id: other.id,
                    label: other.name,
                    title: get_tooltip(other.id, other.description),
                    color: {
                        background: colors.protein,
                        border: colors.protein,
                        highlight: "#FFFF00"
                    }
                });

                var edge_color = get_edge_color(combined_score);
                edges.update({
                    from: protein.id,
                    to: other.id,
                    value: combined_score,
                    title: (combined_score / 1000).toString(),
                    color: {
                        color: edge_color, highlight: edge_color
                    }
                });
            }

            return {
                nodes: nodes,
                edges: edges,
                selected_nodes: selected_nodes
            }
        },
        submit: function(protein) {
            var com = this;

            // wait
            APP.wait = true;
            var progressbar = $("#progressbar");
            progressbar.progressbar("option", "value", false);

            // var threshold = parseFloat(com.threshold);
            var threshold = 0.4;
            $.post(com.api.subgraph, { protein_id: protein.id, threshold: threshold })
                .done(function (subgraph) {
                    var data = com.subgraph_to_visjs_data(subgraph);

                    com.$emit("data-changed", data);
                    com.$emit("last-clicked-changed", $("#protein-btn"));
                    com.$emit("title-changed", protein.name);

                    // wait is over
                    progressbar.progressbar("option", "value", 0);
                    APP.wait = false;
                });
        }
    },
    mounted: function() {
        var com = this;
        // jQuery autocomplete
        $("#protein-input").autocomplete({
            source: (request, response) => {
                // GET request
                $.get(com.api.search, { query: $("#protein-input").val(), species_id: com.species.ncbi_id })
                    .done(function (data) {
                        data.forEach((e) => {
                            com.suggested_protein_list[e.protein_name] = {
                                id: e.protein_id
                            };
                        });
                        response(data.map(x => x.protein_name));
                    });
            },
            select: (event, ui) => {
                var protein_name = ui["item"]["value"];
                var protein = com.suggested_protein_list[protein_name];
                protein.name = protein_name;
                com.$emit("protein-selected", protein);
                com.submit(protein);
            }
        });
    },
    template: `
        <div class="col-md-4 ui-widget">
            Protein:
            <br/>
            <input id="protein-input"
                   type="text"
                   v-bind:disabled="$root.wait">
            </input>
        </div>
    `
});