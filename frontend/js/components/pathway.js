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
        submit: function(pathway) {
            var com = this;

            // wait
            APP.wait = true;
            var progressbar = $("#progressbar");
            progressbar.progressbar("option", "value", false);

            // var threshold = parseFloat(com.threshold);
            var threshold = 0.4;
            $.post(com.api.subgraph, { pathway_id: pathway.id, threshold: threshold })
                .done(function (subgraph) {
                    var data = json_to_visjs_data(subgraph);

                    if (data.nodes_protein.get().length > 0) {
                        com.$emit("data-tree-added", {
                            name: pathway.name,
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
                com.submit(pathway);
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
        </div>
    `
});