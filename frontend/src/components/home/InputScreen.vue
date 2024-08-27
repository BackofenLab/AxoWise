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
          <div class="form-selection">
            <a>Species:</a>
            <v-select v-model="selected_species" :options="species"></v-select>
          </div>
          <div class="form-selection">
            <div class="form-heading">
              <a>Protein list:</a>
              <button id="test-btn" @click="random_proteins()">sample</button>
            </div>
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
          <div class="form-selection">
            <div class="form-heading">
              <a>Edge score:</a>
              <input
                type="number"
                v-bind:min="threshold.min"
                v-bind:max="threshold.max"
                v-bind:step="threshold.step"
                v-model="threshold.value"
                v-on:input="valueChanged('scoregraph')"
              />
            </div>
            <input
              id="scoregraph"
              type="range"
              v-bind:min="threshold.min"
              v-bind:max="threshold.max"
              v-bind:step="threshold.step"
              v-model="threshold.value"
              v-on:input="valueChanged('scoregraph')"
            />
          </div>
          <button
            id="submit-btn"
            @click="submit()"
            :class="{ loading: isAddClass }"
          >
            <span class="button__text">Submit</span>
          </button>
        </div>
      </div>
    </div>
    <div class="social-media">
      <img src="@/assets/socials/youtube.png" />
      <img src="@/assets/socials/git.png" />
      <img src="@/assets/socials/reddit.png" />
      <img src="@/assets/socials/linkedin.png" />
    </div>
  </div>
</template>

<script>
import validator from "validator";

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
        max: 1,
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

      var cleanData = validator.whitelist(this.raw_text, "a-zA-Z0-9\\s");

      // Creating FormData to send files & parameters with an ajax call

      formData.append("threshold", this.threshold.value);
      formData.append("species_id", this.selected_species.code);
      formData.append("proteins", cleanData.split(/\s+/).join(";"));

      this.isAddClass = true;
      this.axios.post(this.api.subgraph, formData).then((response) => {
        if (response.data.length != 0) {
          response.edge_thick = this.edge_thick.value;
          this.isAddClass = false;
          this.$store.commit("assign", response);
          this.$router.push("protein");
        } else {
          alert("no proteins were found.");
          this.isAddClass = false;
        }
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
#test-btn {
  text-transform: lowercase;
  color: #fff;
  background: #0a0a1a57;
  border: none;
  padding: 0.6rem;
  height: 59%;
  display: flex;
  justify-content: center;
  -webkit-align-items: center;
  margin-left: 0.4rem;
  text-align: center;
  align-self: center;
  width: 3.5rem;
}

.input-form-data input[type="number"] {
  text-transform: lowercase;
  color: #fff;
  background: #0a0a1a57;
  border: none;
  padding: 0.6rem;
  height: 59%;
  display: flex;
  text-align: center;
  align-self: center;
  -webkit-align-items: center;
  margin-left: 0.4rem;
  -moz-appearance: textfield;
  -webkit-appearance: textfield;
  appearance: textfield;
  width: 3.5rem;
}

.input-form-data input[type="range"]::-webkit-slider-thumb {
  background: #fafafa;
  appearance: none;
  box-shadow: 1px 2px 26px 1px #bdbdbd;
  width: 0.6rem;
  height: 0.6rem;
}

.form-selection {
  display: grid;
  width: 100%;
  grid-template-columns: 1fr;
  grid-template-rows: 1.5rem 1fr;
  grid-row-gap: 0;
  text-align: left;
}

.form-selection a {
  align-self: center;
}

.form-heading {
  display: flex;
  grid-template-columns: 1fr 1fr;
}

.social-media {
  position: fixed;
  display: flex;
  right: 1rem;
  bottom: 1rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 10px;
}

.social-media img {
  padding: 0.5rem;
  width: 2.5rem;
  height: 2.5rem;
}
</style>
