<template>
  <div class="input-card">
      <div class="input-card-logo">
        <img src="@/assets/logo.png">
      </div>

      <div class="input-card-header">
          <h2>Protein Graph Database</h2>
      </div>

      <div class="input-card-navigation">
        <router-link to="/input">Input</router-link> |
        <router-link to="/file">File</router-link> |
        <router-link to="/import">Import</router-link>
      </div>

      <div class="input-data">
          <div class="input field">
              <div class="input-form-data">
                <button id="test" @click="submit('test')" > Test Sample</button>
                <h4>Species:</h4>
                <v-select v-model="selected_species" :options="species"></v-select>
                <h4>Protein list:</h4>
                <textarea ref="protein_list_input" id="protein-list" v-model="raw_text" rows="10" cols="30" autofocus>
                </textarea>
                <button id="submit-btn" @click="submit()" :class="{'loading': isAddClass}">
                  <span class="button__text" onClick="this.disabled=true;">Submit</span>
                </button>
              </div>
          </div>
      </div>
    </div>
</template>

<script>
export default {
  name: 'InputScreen',

  data() {
    return {
      isAddClass: false,
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
      raw_text: null,
      selected_species: "",
    };
  },

  methods: {
    submit(mode) {

      /*
      Submit function connects the backend with frontend by supplying the user input and retrieving the graph network.

      Transmitting:
        - species id
        - protein list
        - protein threshold

      Retrieving:
        - gephi_json (data structure of graph network)
      */
      this.isAddClass=true;

      var formData = new FormData();
      if(mode == "test"){
        formData.append("proteins", this.$store.state.test_sample);
        formData.append("threshold", this.threshold.value);
        formData.append("species_id", '10090')
      }else{
        //Detection of empty inputs
        if (this.selected_species == "") {
          alert("Please select a species!");
          return;
        }

        if ((this.raw_text == null || this.raw_text == "")) {
          alert("Please provide a list of proteins!");
          return;
        }

        // Creating FormData to send files & parameters with an ajax call
        
        formData.append("threshold", this.threshold.value);
        formData.append("species_id", this.selected_species.code);
        formData.append("proteins", this.raw_text.split("\n").join(";"));
      }


      this.axios
        .post(this.api.subgraph, formData)
        .then((response) => {
          response.edge_thick = this.edge_thick.value;
          this.isAddClass=false;
          this.$store.commit('assign', response)
          this.$router.push("protein")
        })
    }
  }
}



</script>

