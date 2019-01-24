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

            // Vue.js
            APP.visualization.title = "";

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