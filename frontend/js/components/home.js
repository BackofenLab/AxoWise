Vue.component("home", {
  model: {
    props: ["gephi_json", "protein_graph_save", "term_graph_save"],
    event: "gephi-json-changed",
  },
  data: function () {
    return {
      species: [{
        label: 'Mus musculus (mouse)', code: '10090'
      }],
      api: {
        subgraph: "api/subgraph/proteins",
      },
      threshold: {
        value: 0.7,
        min: 0.4,
        max: 1.0,
        step: 0.001,
      },
      edge_thick: {
        value: 0.2,
        min: 0,
        max: 1.0,
        step: 0.1,
      },
      export_file: "graph",
      raw_text: null,
      single_text: null,
      protein_file: null,
      selected_species: "",
      dcoloumns: [],
      selected_d: [],
      check_file: false,
      selected_system: "Multiple",
    };
  },
  methods: {
    submit: function () {
      var com = this;
      protein_file = document.getElementById("protein-file");

      if (com.selected_species == "") {
        alert("Please select a species!");
        return;
      }

      if (
        (com.raw_text == null && protein_file.files.length == 0) ||
        (com.raw_text == "" && protein_file.files.length == 0)
      ) {
        alert("Please provide a list of proteins!");
        return;
      }

      
      $("#submit-btn").addClass("loading");
      

      // Creating FormData to send files & parameters with an ajax call
      formData = new FormData();
      if (protein_file == null) {
        formData.append("proteins", com.raw_text.split("\n").join(";"));
      } else {
        formData.append("file", protein_file.files[0]);
      }
      formData.append("threshold", com.threshold.value);
      formData.append("species_id", com.selected_species.code);
      formData.append("selected_d", com.selected_d);
      
      $.ajax({
        type: "POST",
        url: com.api.subgraph,
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
      }).done(function (json) {
        $("#submit-btn").removeClass("loading");
        com.dcoloumns = [];
        if (Object.keys(json).length == 0) {
          alert("No associations found");
          com.$emit("gephi-json-changed", null);
        } else {
          // save protein graph
          com.$emit("protein-graph-save", json);
          json.edge_thick = com.edge_thick.value;
          com.$emit("gephi-json-changed", json);
        }
      });
      $.ajax({
        type: "POST",
        url: "/api/subgraph/terms",
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
      }).done(function (json) {
        $("#term-btn").removeClass("loading");
        if (Object.keys(json).length != 0) {
          // save term graph
          com.$emit("term-graph-save", json);
        }
      }).fail(function ( jqXHR, textStatus, errorThrown ) {
          console.log(jqXHR);
          console.log(textStatus);
          console.log(errorThrown);
      });
    },
    updateSlider: function () {
      this.eventHub.$emit("edge-update", this.edge_thick.value);
    },
    exportGraph: function () {
      this.eventHub.$emit(
        "export-graph",
        0 === this.export_file.length ? "graph.png" : this.export_file + ".png"
      );
    },
    load_file: function (e) {
      var com = this;

      //Read csv file to get coloumn information
      com.dcoloumns = [];
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = function (e) {
        var allTextLines = e.target.result.split(/\n|\n/);
        var save_dcoloumns = allTextLines[0].split(",");
        var type_coloumns = allTextLines[1].split(",");

        //Return only coloumns that contends for d-value
        for (var i = 0; i < save_dcoloumns.length; i++) {
          if (com.onlyNumbers(type_coloumns[i])) {
            com.dcoloumns.push(save_dcoloumns[i].replace(/^"(.*)"$/, "$1"));
          }
        }
      };
      reader.readAsText(file);
      com.check_file = true;
    },
    onlyNumbers: function (str) {
      return /^[0-9.,-]+$/.test(str);
    },
    load_json: function(e) {
        var com = this;

        //Load json file and overwrite to gephi_json
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = function(e) {
            jsonObj = JSON.parse(e.target.result);
            com.$emit("gephi-json-changed", jsonObj);
          }
        reader.readAsText(file);
    },
  },
  mounted: function () {
    var com = this;

    //Interaction capture of html elements
    $("#submit-btn").button();
    $("#submit-btn").click(com.submit);
    $("#edge-slider").slider();
    $("#edge-slider").change(com.updateSlider);
    $("#edge-input").change(com.updateSlider);
    $("#export-btn").button();
    $("#export-btn").click(com.exportGraph);

    //Change text on input fields according to selected file
    $("form").on("change", "#protein-file", function () {
      $(this)
        .parent(".file-upload-wrapper")
        .attr(
          "data-text",
          $(this)
            .val()
            .replace(/.*(\/|\\)/, "")
        );
    });
  },
  template: `
        <div class="input-card">
            <div class="input-card-logo">
            <img src="images/logo.png" alt="logo">
            </div>

            <div class="input-card-header">
                <h2>Protein Graph Database</h2>
            </div>

            <div class="input-card-navigation">
                <a href="#" @click.prevent="selected_system ='Multiple'" >Inputs</a>
                <a href="#" @click.prevent="selected_system ='File'" >File</a>
                <a href="#" @click.prevent="selected_system ='Import'" >Import</a>
            </div>

            <div class="input-data">

                <div class="input field">

                    <div class="input-form-data">



                        <div v-if="selected_system==='File' || selected_system==='Multiple'">
                            <h4>Species:</h4>
                            <v-select v-model="selected_species" :options="species"></v-select>
                        </div>

                        <div v-if="selected_system==='Import'">
                            <h4>Import your graph:</h4>
                            <div class="file-upload-wrapper" data-text="Select Json">
                            <input type="file" id="graph-file" accept=".json" v-on:change="load_json">
                            </div>
                        </div>

                        <div v-if="selected_system==='Multiple'">
                        <h4>Protein list:</h4>
                        <textarea ref="protein_list_input" id="protein-list" v-model="raw_text" rows="10" cols="30" autofocus></textarea>
                        </div>

                        <div v-if="selected_system==='File'">
                            <h4>Protein file:</h4>
                            <div class="file-upload-wrapper" data-text="Select your file">
                            <input type="file" id="protein-file" accept=".csv" v-on:change="load_file">
                            </div>
                        </div>

                        <div v-show="check_file != false">
                        <h4>D Coloumns:</h4>
                        <v-select multiple v-model="selected_d" :options="dcoloumns"></v-select>
                        </div>
                        <!--<h4>Score threshold:</h4>
                        <input id="threshold-slider"
                            type="range"
                            v-bind:min="threshold.min"
                            v-bind:max="threshold.max"
                            v-bind:step="threshold.step"
                            v-model="threshold.value"
                        />-->
                        <button id="submit-btn" >
                           <span class="button__text" onClick="this.disabled=true;">Submit</span>
                        </button>
                    </div>
                </div>
            </div>

            <div class="input-card-footer">

            </div>
    </div>
`,
});
