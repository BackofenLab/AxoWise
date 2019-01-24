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
        submit: function() {
            var com = this;

            // wait
            APP.wait = true;
            var progressbar = $("#progressbar");
            progressbar.progressbar("option", "value", false);

            var threshold = parseFloat(com.threshold);
            $.get(com.api.subgraph, { protein_id: com.protein.id, threshold: threshold })
                .done(function (subgraph) {
                    var data = protein_subgraph_to_visjs_data(subgraph);
                    NETWORK_DATA_ALL = data;
                    visualize_visjs_data(data);

                    // Vue.js
                    APP.visualization.title = com.protein.name;
                    APP.last_clicked = $("#protein-btn");

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