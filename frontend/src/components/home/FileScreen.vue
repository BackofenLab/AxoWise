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
                  <h4>Species:</h4>
                  <v-select v-model="selected_species" :options="species"></v-select>
                  <h4>Protein file:</h4>
                  <div class="file-upload-wrapper" :data-text="fileuploadText">
                    <input type="file" id="protein-file" accept=".csv" v-on:change="load_file">                  
                  </div>
                  <div v-if="dcoloumns != null">
                    <h4>D Coloumns:</h4>
                    <v-select multiple v-model="selected_d" :options="dcoloumns" :close-on-select="false"></v-select>
                  </div>
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
  name: 'FileScreen',
  data() {
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
      fileuploadText: 'Select your file',
      dcoloumns: null,
      selected_d: [],
      selected_species: null,
      isAddClass: false
    }
  },
  methods: {
    load_file(e) {
      var com = this;

      //Read csv file to get coloumn information
      com.dcoloumns = [];
      const file = e.target.files[0];
      com.fileuploadText = file.name
      const reader = new FileReader();
      reader.onload = function (e) {
        var allTextLines = e.target.result.split(/\n|\n/);
        var save_dcoloumns = allTextLines[0].split(",");
        var type_coloumns = allTextLines[1].split(",");

        //Return only coloumns that contends for d-value
        for (var i = 0; i < save_dcoloumns.length; i++) {
          type_coloumns[i]=type_coloumns[i].trim()
          if (com.onlyNumbers(type_coloumns[i])) {
            save_dcoloumns[i]=save_dcoloumns[i].trim()
            com.dcoloumns.push(save_dcoloumns[i].replace(/^"(.*)"$/, "$1"));
          }
        }
      };
      reader.readAsText(file);
    },
    onlyNumbers(possibleNumber) {
      return /^[0-9.,-]+$/.test(possibleNumber);
    },
    submit() {
      var com = this
      
      

      if (com.selected_species == "") {
        alert("Please select a species!");
        return;
      }

      const protein_file = document.getElementById("protein-file");

      if(protein_file.files.length == 0 || protein_file == null){
        alert("Please supply a file!");
        return;
      }

      
      var formData = new FormData();
      formData.append("threshold", com.threshold.value);
      formData.append("species_id", com.selected_species.code);
      formData.append("file", protein_file.files[0]);
      formData.append("selected_d", com.selected_d);
      
      this.$store.commit('assign_dcoloumn', com.selected_d)
      
      com.isAddClass=true;
      this.axios
        .post(this.api.subgraph, formData)
        .then((response) => {
          com.isAddClass=false;
          response.edge_thick = 0.01;
          com.$store.commit('assign', response)
          com.$router.push("protein")
        })
    }
  }
}
</script>

  