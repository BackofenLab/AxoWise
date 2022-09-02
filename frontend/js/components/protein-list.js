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
            export_file: "graph",
            raw_text: null,
            protein_file: null,
            selected_species: null,
            d_value: false
        }
    },
    methods: {
        submit: function() {
            var com = this;
            protein_file = document.getElementById("protein-file");

            if (com.selected_species == null) {
                alert("Please select a species!");
                return;
            }

            if (com.raw_text == null && protein_file.files.length == 0 || com.raw_text == "" && protein_file.files.length == 0) {
                alert("Please provide a list of proteins!");
                return;
            }
            
            // Creating FormData to send files & parameters with an ajax call
            protein_list = protein_file.files[0];
            formData = new FormData();
            if(protein_file.files.length == 0){
                formData.append('proteins', com.raw_text.split('\n').join(';'));
            }else{
                formData.append('file', protein_list);
            }
            formData.append('threshold', com.threshold.value);
            formData.append('species_id', com.selected_species);
            
            $("body").addClass("loading");         

            $.ajax({
                type: 'POST',
                url: com.api.subgraph,
                data: formData,
                contentType: false,
                cache: false,
                processData: false,
              })
                .done(function (json) {
                    $("body").removeClass("loading");
                    if(Object.keys(json).length == 0){
                         com.$emit("gephi-json-changed", null);
                    }else{
                        json.edge_thick = com.edge_thick.value;
                        com.$emit("gephi-json-changed", json);
                    }
            });
        },
        updateSlider: function(){
            this.eventHub.$emit('edge-update', this.edge_thick.value);
        },
        exportGraph: function(){
            this.eventHub.$emit('export-graph', (0 === this.export_file.length) ? 'graph.png' : this.export_file + '.png');
        }
    },
    mounted: function() {
        var com = this;
        $("#submit-btn").button();
        $("#submit-btn").click(com.submit);
        $("#edge-slider").slider();
        $("#edge-slider").change(com.updateSlider);
        $("#edge-input").change(com.updateSlider); //update from input control
        $("#export-btn").button();
        $("#export-btn").click(com.exportGraph);
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

            <h4>Protein file:</h4>
            <input type="file" id="protein-file" accept=".csv">
            <br/><br/>

            <h4>Apply D_Value:</h4>
            <input type="checkbox" id="d_value" v-model="d_value" checked>
            <br/><br/>

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
             <div style="display: flex">
               <button id="export-btn" type="export">Export Graph</button>
               <input id="file_name"
                type="text"
                v-model="export_file"
               />
             </div>
            <br/><br/>
        </div>
`
});