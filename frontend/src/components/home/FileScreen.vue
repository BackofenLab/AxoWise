<template>
  <div class="input-card">
    <div class="input-card-logo">
      <img src="@/assets/logo.png" />
    </div>

    <div class="input-card-header">
      <h2>Protein Graph Database</h2>
    </div>

    <div class="input-card-navigation">
      <router-link to="/input">Input</router-link>
      <router-link to="/file">File</router-link>
      <router-link to="/import">Import</router-link>
    </div>

    <div class="input-data">
      <div class="input field">
        <div class="input-form-data">
          <div class="species-selection">
            <a>Species:</a>
            <v-select v-model="selected_species" :options="species"></v-select>
          </div>
          <h4>Protein file:</h4>
          <div class="file-upload-wrapper" :data-text="fileuploadText">
            <input
              type="file"
              id="protein-file"
              accept=".csv"
              v-on:change="load_file"
            />
          </div>
          <div id="coloumn-selection" v-if="dcoloumns != null">
            <h4>D Coloumns:</h4>
            <button id="test-btn" @click="select_all">select all</button>
            <div class="filter-section">
              <div
                id="pathway-filter"
                class="pre-full colortype"
                v-on:click="handling_filter_menu()"
                :class="{ full: dcoloumn_filtering == true }"
              >
                <span>{{ coloumn }}</span>
                <img
                  class="remove-filter"
                  src="@/assets/pathwaybar/cross.png"
                  v-on:click.stop="active_categories(null)"
                  v-if="coloumn !== 'Filter'"
                />
              </div>
              <div
                id="home-filter-categories"
                class="colortype"
                v-show="dcoloumn_filtering == true"
              >
                <div
                  class="element"
                  v-for="(entry, index) in dcoloumns"
                  :key="index"
                  v-on:click="active_categories(entry)"
                  :class="{ active_cat: active_categories_set.has(entry) }"
                >
                  <a>{{ entry }}</a>
                </div>
              </div>
            </div>
          </div>
          <h4>Edge score:</h4>
          <input
            id="scoregraph"
            type="range"
            v-bind:min="threshold.min"
            v-bind:max="threshold.max"
            v-bind:step="threshold.step"
            v-model="threshold.value"
            v-on:input="valueChanged('scoregraph')"
          />
          <input
            type="number"
            v-bind:min="threshold.min"
            v-bind:max="threshold.max"
            v-bind:step="threshold.step"
            v-model="threshold.value"
            v-on:input="valueChanged('scoregraph')"
          />
          <button
            id="submit-btn"
            @click="submit()"
            :class="{ loading: isAddClass }"
          >
            <span class="button__text" onClick="this.disabled=true;"
              >Submit</span
            >
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FileScreen",
  data() {
    return {
      species: [
        {
          label: "Mus musculus (mouse)",
          code: "10090",
        },
        {
          label: "Homo sapiens (human)",
          code: "9606",
        },
      ],
      api: {
        subgraph: "api/subgraph/proteins",
      },
      threshold: {
        value: 0,
        min: 0,
        max: 0.9999,
        step: 0.01,
      },
      fileuploadText: "Select your file",
      dcoloumns: null,
      selected_d: [],
      selected_species: null,
      isAddClass: false,
      dcoloumn_filtering: false,
      coloumn: "Filter",
      active_categories_set: new Set(),
    };
  },
  methods: {
    select_all() {
      this.active_categories_set = new Set(this.dcoloumns);
      this.coloumn = [...this.active_categories_set].join(", ");
    },
    active_categories(coloumn) {
      if (!coloumn) {
        this.reset_categories();
        return;
      }
      if (this.active_categories_set.has(coloumn)) {
        if (this.active_categories_set.size == 1) {
          this.reset_categories();
          return;
        }
        this.active_categories_set.delete(coloumn);
      } else {
        this.active_categories_set.add(coloumn);
      }
      this.coloumn = [...this.active_categories_set].join(", ");
    },
    reset_categories() {
      this.coloumn = "Filter";
      this.active_categories_set = new Set();
    },
    handling_filter_menu() {
      var com = this;
      if (!com.dcoloumn_filtering) {
        com.dcoloumn_filtering = true;

        // Add the event listener
        document.addEventListener("mouseup", com.handleMouseUp);
      } else {
        com.category_filtering = false;
        document.removeEventListener("mouseup", com.handleMouseUp);
      }
    },
    handleMouseUp(e) {
      var com = this;

      var container = document.getElementById("home-filter-categories");
      var container_button = document.getElementById("pathway-filter");
      if (
        !container.contains(e.target) &&
        !container_button.contains(e.target)
      ) {
        com.dcoloumn_filtering = false;

        // Remove the event listener
        document.removeEventListener("mouseup", com.handleMouseUp);
      }
    },
    load_file(e) {
      var com = this;

      //Read csv file to get coloumn information
      com.dcoloumns = [];
      const file = e.target.files[0];
      com.fileuploadText = file.name;
      const reader = new FileReader();
      reader.onload = function (e) {
        var allTextLines = e.target.result.split(/\n|\n/);
        var save_dcoloumns = allTextLines[0].split(",");
        var type_coloumns = allTextLines[1].split(",");

        //Return only coloumns that contends for d-value
        for (var i = 0; i < save_dcoloumns.length; i++) {
          type_coloumns[i] = type_coloumns[i].trim();
          if (com.onlyNumbers(type_coloumns[i])) {
            save_dcoloumns[i] = save_dcoloumns[i].trim();
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
      var com = this;

      if (com.selected_species == "") {
        alert("Please select a species!");
        return;
      }

      const protein_file = document.getElementById("protein-file");

      if (protein_file.files.length == 0 || protein_file == null) {
        alert("Please supply a file!");
        return;
      }

      var formData = new FormData();
      formData.append("threshold", com.threshold.value);
      formData.append("species_id", com.selected_species.code);
      formData.append("file", protein_file.files[0]);
      formData.append("selected_d", [...com.active_categories_set]);

      this.$store.commit("assign_dcoloumn", [...this.active_categories_set]);

      com.isAddClass = true;
      this.axios.post(this.api.subgraph, formData).then((response) => {
        com.isAddClass = false;
        response.edge_thick = 0.01;
        com.$store.commit("assign", response);
        com.$router.push("protein");
      });
    },
    valueChanged(id) {
      var target = document.getElementById(id);
      let a = (target.value / target.max) * 100;
      target.style.background = `linear-gradient(to right,#0A0A1A,#0A0A1A ${a}%,#ccc ${a}%)`;
    },
  },
};
</script>
<style>
#home-filter-categories {
  position: absolute;
  max-height: 600%;
  width: 100%;
  left: 0;
  top: 100%;
  padding: 0.3% 0 0.3% 0;
  border-radius: 0 0 5px 5px;
  -webkit-backdrop-filter: blur(7.5px);
  backdrop-filter: blur(7.5px);
  overflow-y: scroll;
  overflow-x: hidden;
  color: #fff;
  border-color: hsla(0, 0%, 100%, 0.3);
  border-width: 1px;
  border-style: solid;
  z-index: 999;
}

#coloumn-selection .filter-section {
  width: 100%;
  height: 3vw;
  display: flex;
  position: relative;
  left: 0;
  background: rgba(0, 0, 0, 0.7);
}
</style>
