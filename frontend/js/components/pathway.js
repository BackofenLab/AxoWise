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
        subgraph_to_visjs_data: function(subgraph) {
            var nodes = new vis.DataSet();
            var edges = new vis.DataSet();
        
            for (var i = 0; i < subgraph.classes.length; i++) {
                var klass = subgraph.classes[i];
        
                nodes.update({
                    id: klass.name,
                    label: klass.name,
                    color: colors.gray
                });
            }
        
            for (var i = 0; i < subgraph.proteins.length; i++) {
                var protein = subgraph.proteins[i];
        
                nodes.update({
                    id: protein.id,
                    label: protein.name,
                    title: get_tooltip(protein.id, protein.description),
                    color: colors.protein
                });
            }
        
            for (var i = 0; i < subgraph.associations.length; i++) {
                var entry = subgraph.associations[i];
                var protein1_id = entry.protein1_id;
                var combined_score = entry.combined_score;
                var protein2_id = entry.protein2_id;
        
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

            // var threshold = parseFloat(com.threshold);
            var threshold = 0.4;
            $.post(com.api.subgraph, { pathway_id: com.pathway.id, threshold: threshold })
                .done(function (subgraph) {
                    var data = com.subgraph_to_visjs_data(subgraph);

                    com.$emit("data-changed", data);
                    com.$emit("last-clicked-changed", $("#pathway-btn"));
                    com.$emit("title-changed", com.pathway.name);

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