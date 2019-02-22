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
                    var data = json_to_visjs_data(subgraph);

                    if (data.nodes_protein.get().length > 0) {
                        com.$emit("data-tree-added", {
                            name: protein.name,
                            data: data,
                            index: [],
                            children: []
                        });
                    }

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