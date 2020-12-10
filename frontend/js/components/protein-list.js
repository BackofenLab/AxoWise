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
                min: 0.4,
                max: 1.0,
                step: 0.001
            },
            edge_thick: {
                value: 0.2,
                min: 0,
                max: 1.0,
                step: 0.1
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
                    json.edge_thick = com.edge_thick.value;
                    $("body").removeClass("loading");
                    com.$emit("gephi-json-changed", json);
            });
        },
        updateSlider: function (){
            this.eventHub.$emit('edge-update', this.edge_thick.value);
        }
    },
    mounted: function() {
        var com = this;
        $("#submit-btn").button();
        $("#submit-btn").click(com.submit);
        $("#edge-slider").slider();
        $("#edge-slider").change(com.updateSlider);

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
            <textarea ref="protein_list_input" id="protein-list" v-model="raw_text" rows="10" cols="30" autofocus></textarea><br/>
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
            <br/><br/>
            <h4>Edge Color thickness</h4>
              <input id="edge-slider"
                type="range"
                v-bind:min="edge_thick.min"
                v-bind:max="edge_thick.max"
                v-bind:step="edge_thick.step"
                v-model="edge_thick.value"
            />
            <input id="edge-input"
                type="number"
                v-bind:min="edge_thick.min"
                v-bind:max="edge_thick.max"
                v-bind:step="edge_thick.step"
                v-model="edge_thick.value"
            />
            <br/><br/>
        </div>
`
});