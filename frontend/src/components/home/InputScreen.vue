<template>
  <div class="input-card">
    <div class="input-card-logo">
      <img src="@/assets/logo.png" />
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
          <div class="input-field-protein">
            <h4>Protein list:</h4>
            <button id="test-btn" @click="random_proteins">sample</button>
            <textarea
              ref="protein_list_input"
              id="protein-list"
              v-model="raw_text"
              rows="10"
              cols="30"
              autofocus
            >
            </textarea>
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
  name: "InputScreen",

  data() {
    return {
      isAddClass: false,
      species: [
        {
          label: "Mus musculus (mouse)",
          code: "10090",
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
      edge_thick: {
        value: 0.2,
      },
      raw_text: null,
      selected_species: "",
    };
  },

  methods: {
    submit() {
      /*
      Submit function connects the backend with frontend by supplying the user input and retrieving the graph network.

      Transmitting:
        - species id
        - protein list
        - protein threshold

      Retrieving:
        - gephi_json (data structure of graph network)
      */

      var formData = new FormData();
      //Detection of empty inputs
      if (this.selected_species == "") {
        alert("Please select a species!");
        return;
      }

      if (this.raw_text == null || this.raw_text == "") {
        alert("Please provide a list of proteins!");
        return;
      }

      // Creating FormData to send files & parameters with an ajax call

      formData.append("threshold", this.threshold.value);
      formData.append("species_id", this.selected_species.code);
      formData.append("proteins", this.raw_text.split("\n").join(";"));

      this.isAddClass = true;
      this.axios.post(this.api.subgraph, formData).then((response) => {
        response.edge_thick = this.edge_thick.value;
        this.isAddClass = false;
        this.$store.commit("assign", response);
        this.$router.push("protein");
      });
    },
    async random_proteins() {
      const response = await fetch("./mousedb.csv");
      if (!response.ok) {
        throw new Error("HTTP error " + response.status);
      }
      const text = await response.text();
      var randomProteins = this.getRandomElements(text.split(/[\r\n]+/), 600);

      this.raw_text = randomProteins.join("\n");
    },
    getRandomElements(array, numElements) {
      const randomElements = [];
      const arrayCopy = array.slice(); // Create a copy of the original array

      while (randomElements.length < numElements && arrayCopy.length > 0) {
        const randomIndex = Math.floor(Math.random() * arrayCopy.length);
        const randomElement = arrayCopy.splice(randomIndex, 1)[0];
        randomElements.push(randomElement);
      }

      return randomElements;
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
.input-field-protein {
  display: block;
}

#test-btn {
  margin: 0 0 6px 0;
  text-transform: lowercase;
  padding: 3px;
  font-size: 9px;
}

.input-form-data input[type="number"] {
  border: none;
  border-radius: 5px;
  text-align: center;
  font-family: "ABeeZee", sans-serif;
  background: none;
  -moz-appearance: textfield;
  -webkit-appearance: textfield;
  appearance: textfield;
}

.input-form-data input[type="range"] {
  appearance: none;
  outline: none;
  width: 10vw;
  height: 0.3vw;
  border-radius: 5px;
  background-color: #ccc;
}
.input-form-data input[type="range"]::-webkit-slider-thumb {
  background: #fafafa;
  appearance: none;
  box-shadow: 1px 2px 26px 1px #bdbdbd;
  width: 0.8vw;
  height: 0.8vw;
  border-radius: 50%;
}
</style>
