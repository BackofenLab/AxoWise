Vue.component("protein-list", {
    model: {
        prop: "gephi_json",
        event: "gephi-json-changed"
    },
    data: function() {
        return {
            api: {
                subgraph: "api/subgraph/proteins"
            },
            raw_text: null
        }
    },
    methods: {
        submit: function() {
            var com = this;

            $("body").addClass("loading");

            $.post(com.api.subgraph, {
                proteins: com.raw_text.split('\n').join(';'),
                // TODO threshold: threshold
            })
                .done(function (json) {
                    $("body").removeClass("loading");
                    com.$emit("gephi-json-changed", json);
            });
        }
    },
    mounted: function() {
        var com = this;
        $("#submit-btn").button();
        $("#submit-btn").click(com.submit);
    },
    template: `
        <div class="cf"><h2>Protein list:</h2>
            <textarea id="protein-list" v-model="raw_text" rows="10" cols="30"/></textarea><br/>
            <button id="submit-btn">Submit</button>
        </div>
    `
});