Vue.component("species-search", {
    model: {
        prop: "species",
        event: "species-selected"
    },
    props: ["species"],
    data: function() {
        return {
            api: {
                search: "api/search/species",
            },
            suggested_species_list: {}
        }
    },
    mounted: function() {
        var com = this;
        // jQuery autocomplete
        $("#species-input").autocomplete({
            source: (request, response) => {
                // GET request
                $.get(com.api.search, { query: $("#species-input").val() })
                    .done(function (data) {
                        data.forEach((e) => {
                            com.suggested_species_list[e.species_name] = {
                                ncbi_id: e.ncbi_id,
                                kegg_id: e.kegg_id
                            };
                        });
                        response(data.map(x => x.species_name));
                    });
            },
            select: (event, ui) => {
                var species_name = ui["item"]["value"];
                var species = com.suggested_species_list[species_name];
                species.name = species_name;
                com.$emit("species-selected", species);

                // TODO
                APP.wait = false;
            }
        });
    },
    template: `
        <div class="col-md-4 ui-widget">
            Species:
            <br/>
            <input id="species-input" type="text"></input>
        </div>
    `,
});