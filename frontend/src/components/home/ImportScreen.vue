
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
                    <h4>Import your graph:</h4>
                    <div class="file-upload-wrapper" :data-text="fileuploadText">
                    <input type="file" id="graph-file" accept=".json" v-on:change="load_json">
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
  name: 'ImportScreen',
  data(){
    return {
      fileuploadText: 'Select Json',
      gephi_json: null,
      isAddClass: false
    }
  },
  methods: {
    load_json(e) {
      var com = this

    //Load json file and overwrite to gephi_json
    const file = e.target.files[0];
    com.fileuploadText = file.name
    const reader = new FileReader();
    reader.onload = function(e) {
      com.gephi_json = JSON.parse(e.target.result);
      }
    reader.readAsText(file);
   },
   submit() {
    var com = this;

    if (com.gephi_json == null) {
        alert("Please select a import!");
        return;
      }
    com.isAddClass = true
    
    com.$store.commit('assign', { data:com.gephi_json })
    com.$store.commit('assign_dcoloumn', com.gephi_json.dvalues)
    com.$router.push("protein")

    com.isAddClass = false
   }
  }
}
</script>
  
  