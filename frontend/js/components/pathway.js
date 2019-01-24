Vue.component("pathway", {
    model: {
        prop: "pathway",
        event: "pathway-selected"
    },
    props: ["pathway", "species", "threshold"],
    data: function() {
        return {
            api: {
                search: "api/search/pathway",
                subgraph: "api/subgraph/pathway"
            },
            suggested_pathway_list: {}
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
            $.get(com.api.subgraph, { pathway_id: com.pathway.id, threshold: threshold })
                .done(function (subgraph) {
                    var data = pathway_subgraph_to_visjs_data(subgraph);
                    NETWORK_DATA_ALL = data;
                    visualize_visjs_data(data);

                    // Vue.js
                    APP.visualization.title = APP.pathway.name;
                    APP.last_clicked = $("#pathway-btn");

                    // wait is over
                    progressbar.progressbar("option", "value", 0);
                    APP.wait = false;
                });
        }
    },
    mounted: function() {
        var com = this;
        // jQuery autocomplete
        $("#pathway-input").autocomplete({
            source: (request, response) => {
                // GET reqeust
                $.get(com.api.search, { query: $("#pathway-input").val(), species_id: com.species.ncbi_id })
                    .done(function (data) {
                        data.forEach((e) => {
                            com.suggested_pathway_list[e.pathway_name] = {id: e.pathway_id};
                        });
                        response(data.map(x => x.pathway_name));
                    });
            },
            select: (event, ui) => {
                var pathway_name = ui["item"]["value"];
                var pathway = com.suggested_pathway_list[pathway_name];
                pathway.name = pathway_name;
                com.$emit("pathway-selected", pathway);
            }
        });
    },
    template: `
        <div class="col-md-4 ui-widget">
            Pathway:
            <br/>
            <input id="pathway-input"
                   type="text"
                   v-bind:disabled="$root.wait"
            ></input>
            <br/>
            <button id="pathway-btn"
                    class="btn btn-primary btn-xs"
                    v-bind:disabled="$root.wait"
                    v-on:click="submit()"
            >Submit</button>
        </div>
    `
});