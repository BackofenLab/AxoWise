Vue.component("protein-list", {
    model: {
        prop: "protein_list",
        event: "protein-list-changed"
    },
    props: ["protein_list", "species", "threshold"],
    data: function() {
        return {
            api: {
                search: "api/search/protein_list",
                subgraph: "api/subgraph/protein_list"
            },
            raw_text: null
        }
    },
    methods: {
        subgraph_to_visjs_data: function(subgraph) {
            var nodes_protein = new vis.DataSet();
            var nodes_pathway = new vis.DataSet();
            var nodes_class = new vis.DataSet();
            var edges = new vis.DataSet();
            if (!subgraph)
                return {
                    nodes: nodes,
                    edges: edges
                }

            var proteins = subgraph.proteins;
            var pathways = subgraph.pathways;
            var associations = subgraph.associations;

            for (var i = 0; i < proteins.length; i++) {
                var protein = proteins[i];

                nodes_protein.update({
                    id: protein.id,
                    label: protein.name,
                    title: get_tooltip(protein.id, protein.description),
                    color: {
                        background: colors.protein,
                        border: colors.protein,
                        highlight: "#FFFF00"
                    }
                });
            }

            for (var i = 0; i < pathways.length; i++) {
                var pathway = pathways[i];

                nodes_pathway.update({
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
            }

            for (var i = 0; i < associations.length; i++) {
                var association = associations[i];
                var combined_score = association.combined_score;
                var protein1_id = association.protein1_id;
                var protein2_id = association.protein2_id;
                var pathway_id = association.pathway_id;

                var edge_color = get_edge_color(combined_score);
                edges.update({
                    from: protein1_id,
                    to: protein2_id,
                    value: combined_score,
                    title: (combined_score / 1000).toString(),
                    color: {
                        color: edge_color, highlight: edge_color
                    }
                });
                if (pathway_id)
                    edges.update([
                        {
                            from: protein1_id,
                            to: pathway_id,
                            color: colors.pathway
                        },
                        {
                            from: protein2_id,
                            to: pathway_id,
                            color: colors.pathway
                        }
                    ]);
            }

            return {
                nodes_protein: nodes_protein,
                nodes_pathway: nodes_pathway,
                edges: edges
            }
        },
        submit: function() {
            var com = this;

            // wait
            APP.wait = true;
            var progressbar = $("#progressbar");
            progressbar.progressbar("option", "value", false);

            $.get(com.api.search, { query: com.raw_text.split('\n').join(';'), species_id: com.species.ncbi_id })
                    .done(function (data) {
                        var protein_ids = data.map(x => x.protein_id);
                        com.$emit("protein-list-changed", protein_ids);

                        // var threshold = parseFloat(com.threshold);
                        var threshold = 0.4;
                        $.post(com.api.subgraph, { protein_ids: protein_ids.join(';'), threshold: threshold })
                            .done(function (subgraph) {
                                var data = com.subgraph_to_visjs_data(subgraph);
                                var protein_names = data.nodes_protein.get().map(function (node) {
                                    return node.label
                                }).slice(0, 3);

                                if (data.nodes_protein.get().length > 0) {
                                    com.$emit("title-changed", "");
                                    com.$emit("data-tree-added", {
                                        name: protein_names.join(", ") + "...",
                                        data: data,
                                        index: 0,
                                        children: []
                                    });
                                }

                                // wait is over
                                progressbar.progressbar("option", "value", 0);
                                APP.wait = false;
                            });
                    });
        }
    },
    template: `
        <div class="col-md-4 ui-widget">
            Protein list:
            <br/>
            <textarea id="protein-list-input"
                      v-model="raw_text"
                      v-bind:disabled="$root.wait"
            ></textarea>
            <br/>
            <button id="protein-list-btn"
                    class="btn btn-primary btn-xs"
                    v-bind:disabled="$root.wait"
                    v-on:click="submit()"
            ><span class="glyphicon glyphicon-list" aria-hidden="true"></span> Submit</button>
        </div>
    `
});