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
                                var data = json_to_visjs_data(subgraph);
                                var protein_names = data.nodes_protein.get().map(function (node) {
                                    return node.label
                                }).slice(0, 3);

                                if (data.nodes_protein.get().length > 0) {
                                    com.$emit("data-tree-added", {
                                        name: protein_names.join(", ") + "...",
                                        data: data,
                                        index: [],
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