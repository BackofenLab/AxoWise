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
            if (subgraph.length >=1)
                selected_nodes.push(subgraph[0].protein.id);

            for (var i = 0; i < subgraph.length; i++) {
                var row = subgraph[i];
                var protein = row.protein;
                var other = row.other;
                var association = row.association;

                nodes.update({
                    id: protein.id,
                    label: protein.name,
                    title: get_tooltip(protein.id, protein.description),
                    color: colors.protein
                });

                if (other) {
                    nodes.update({
                        id: other.id,
                        label: other.name,
                        title: get_tooltip(other.id, other.description),
                        color: colors.protein
                    });

                    var edge_color = get_edge_color(association.combined);
                    edges.update({
                        from: protein.id,
                        to: other.id,
                        value: association.combined,
                        title: (association.combined / 1000).toString(),
                        color: {
                            color: edge_color, highlight: edge_color
                        }
                    });
                }

                for (var j = 0; j < row.pathways.length; j++) {
                    var pathway = row.pathways[j];

                    nodes.update({
                        id: pathway.id,
                        label: pathway.name,
                        title: get_tooltip(pathway.id, pathway.description),
                        color: colors.pathway,
                        shape: "square"
                    });

                    edges.update([
                        // {
                        //     from: row.protein.id,
                        //     to: pathway.id,
                        //     color: colors.pathway
                        // },
                        {
                            from: row.other.id,
                            to: pathway.id,
                            color: colors.pathway
                        }
                    ]);
                }
            }

            return {
                nodes: nodes,
                edges: edges,
                selected_nodes: selected_nodes
            }
        },
        submit: function() {
            var com = this;

            // wait
            APP.wait = true;
            var progressbar = $("#progressbar");
            progressbar.progressbar("option", "value", false);

            var threshold = parseFloat(com.threshold);
            $.get(com.api.subgraph, { protein_id: com.protein.id, threshold: threshold })
                .done(function (subgraph) {
                    var data = com.subgraph_to_visjs_data(subgraph);

                    com.$emit("data-changed", data);
                    com.$emit("last-clicked-changed", $("#protein-btn"));
                    com.$emit("title-changed", com.protein.name);

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
            <br/>
            <button id="protein-btn"
                    class="btn btn-primary btn-xs"
                    v-bind:disabled="$root.wait"
                    v-on:click="submit()"
            >Submit</button>
        </div>
    `
});