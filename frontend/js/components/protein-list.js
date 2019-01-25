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
            var nodes = new vis.DataSet();
            var edges = new vis.DataSet();

            for (var i = 0; i < subgraph.length; i++) {
                var row = subgraph[i];
                var protein1 = row.protein1;
                var protein2 = row.protein2;
                var association = row.association;
                var pathways = row.pathways;

                nodes.update({
                    id: protein1.id,
                    label: protein1.name,
                    title: get_tooltip(protein1.id, protein1.description),
                    color: colors.protein
                });

                nodes.update({
                    id: protein2.id,
                    label: protein2.name,
                    title: get_tooltip(protein2.id, protein2.description),
                    color: colors.protein
                });

                if (association) {
                    var edge_color = get_edge_color(association.combined);
                    edges.update({
                        from: protein1.id,
                        to: protein2.id,
                        value: association.combined,
                        title: (association.combined / 1000).toString(),
                        color: {
                            color: edge_color, highlight: edge_color
                        }
                    });
                }

                for (var j = 0; j < pathways.length; j++) {
                    var pathway = pathways[j];

                    nodes.update({
                        id: pathway.id,
                        label: pathway.name,
                        title: get_tooltip(pathway.id, pathway.description),
                        color: colors.pathway,
                        shape: "square"
                    });

                    edges.update(
                        {
                            from: protein1.id,
                            to: pathway.id,
                            color: colors.pathway
                        }
                    );
                    edges.update(
                        {
                            from: protein2.id,
                            to: pathway.id,
                            color: colors.pathway
                        }
                    );
                }
            }

            return {
                nodes: nodes,
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

                        var threshold = parseFloat(com.threshold);
                        $.get(com.api.subgraph, { protein_ids: protein_ids.join(';'), threshold: threshold })
                            .done(function (subgraph) {
                                var data = com.subgraph_to_visjs_data(subgraph);

                                com.$emit("data-changed", data);
                                com.$emit("last-clicked-changed", $("#protein-list-btn"));
                                com.$emit("title-changed", "");

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
            >Submit</button>
        </div>
    `
});