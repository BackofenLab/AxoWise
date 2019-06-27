Vue.component("protein-list", {
    model: {
        prop: "gephi_json",
        event: "gephi-json-changed"
    },
    data: function() {
        return {
            species: {
                9606: "Homo sapiens (human)",
                10090: "Mus musculus (mouse)"
            },
            api: {
                subgraph: "api/subgraph/proteins"
            },
            threshold: {
                value: 0.7,
                min: 0.7,
                max: 1.0,
                step: 0.001
            },
            raw_text: null,
            selected_species: null
        }
    },
    methods: {
        submit: function() {
            var com = this;

            if (com.selected_species == null) {
                alert("Please select a species!");
                return;
            }

            if (com.raw_text == null || com.raw_text == "") {
                alert("Please provide a list of proteins!");
                return;
            }

            $("body").addClass("loading");

            $.post(com.api.subgraph, {
                proteins: com.raw_text.split('\n').join(';'),
                threshold: com.threshold.value,
                species_id: com.selected_species,
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
        <div class="cf">
            <h4>Species:</h4>
            <select v-model="selected_species">
                <option disabled value="">Please select species</option>
                <option v-for="(value, key, index) in species" v-bind:value="key">{{value}}</option>
            </select>
            <br/><br/>

            <h4>Protein list:</h4>
            <textarea id="protein-list" v-model="raw_text" rows="10" cols="30"/></textarea><br/>
            <br/>

            <h4>Protein - protein score threshold:</h4>
            <input id="threshold-slider"
                type="range"
                v-bind:min="threshold.min"
                v-bind:max="threshold.max"
                v-bind:step="threshold.step"
                v-model="threshold.value"
            />
            <input id="threshold-input"
                type="number"
                v-bind:min="threshold.min"
                v-bind:max="threshold.max"
                v-bind:step="threshold.step"
                v-model="threshold.value"
            />
            <br/><br/>

            <button id="submit-btn">Submit</button>
        </div>
    `
});