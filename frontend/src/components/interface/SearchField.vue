<template>
  <div id="search-menu">
    <div id="search" class="search-field">
      <img class="search-field-icon" src="@/assets/toolbar/search.png" />
      <input
        type="text"
        v-model="search_raw"
        class="empty"
        placeholder="Find your node"
        @keyup.enter="select_node(filt_search[0])"
      />
    </div>
    <div
      class="check-active"
      v-if="search_raw.length >= 2 && filt_search.length > 0"
      v-on:click="search_raw = ''"
    ></div>
    <div
      class="search-background"
      v-if="search_raw.length >= 2 && filt_search.length > 0"
    ></div>
    <div
      class="results"
      v-if="search_raw.length >= 2 && filt_search.length > 0"
    >
      <div class="result-label">nodes in network</div>
      <div
        v-for="(entry, index) in filt_search"
        :key="index"
        class="network-search"
      >
        <a href="#" v-on:click="select_node(entry)">{{
          entry.attributes["Name"]
        }}</a>
      </div>
      <div class="result-label">search google</div>
      <div
        v-for="(entry, index) in filt_search"
        :key="index"
        class="google-search"
      >
        <img class="google-logo" src="@/assets/toolbar/google-logo.png" />
        <a
          :id="'results-' + index"
          href=""
          v-on:click="google_search(entry.attributes['Name'], index)"
          target="_blank"
          >{{ entry.attributes["Name"] }}</a
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchField",
  props: ["data", "mode"],
  data() {
    return {
      search_raw: "",
    };
  },
  methods: {
    select_node(node) {
      if (node)
        this.emitter.emit("searchNode", { node: node, mode: this.mode });
    },
    google_search(protein, index) {
      document
        .getElementById("results-" + index)
        .setAttribute("href", "https://www.google.com/search?q=" + protein);
    },
  },
  computed: {
    regex() {
      var com = this;
      return RegExp(
        com.search_raw.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
      );
    },
    filt_search() {
      var com = this;
      var matches = [];

      if (com.search_raw.length >= 2) {
        var regex = new RegExp(com.regex, "i");
        matches = com.data.nodes.filter(function (node) {
          return regex.test(node.label) || regex.test(node.attributes.Alias);
        });
      }
      return matches;
    },
  },
};
</script>

<style>
#search-menu {
  height: 5%;
  display: flex;
  width: 100%;
  position: relative;
  align-content: center;
  justify-content: center;
  z-index: 9999;
  margin-bottom: 2%;
}

#search-menu:after {
  content: "";
  position: absolute;
  z-index: 1;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  backdrop-filter: blur(7.5px);
}

.search-field {
  width: 100%;
  height: 100%;
  display: flex;
  background: rgba(222, 222, 222, 0.3);
  position: absolute;
  align-items: center;
  align-content: center;
  justify-content: center;
  z-index: 999;
}

.search-field-icon {
  position: absolute;
  left: 3%;
  height: 0.9vw;
  width: 0.9vw;
  filter: invert(100%);
}

.search-field input[type="text"] {
  margin-left: 2%;
  font-size: 0.85vw;
  width: 83%;
  background: none;
  color: white;
  cursor: default;
  font-family: "ABeeZee", sans-serif;
  border: none;
}

.search-field [type="text"]::-webkit-input-placeholder {
  opacity: 70%;
}

#search-menu .results {
  position: absolute;
  width: 100%;
  left: 0%;
  top: 100%;
  padding: 0.3% 0 0.3% 0;
  background: rgba(222, 222, 222, 0.3);
  backdrop-filter: blur(7.5px);
  overflow-y: scroll;
  overflow-x: hidden;
  color: white;
  border-top-color: rgba(255, 255, 255, 30%);
  border-top-width: 1px;
  border-top-style: solid;
  z-index: 999;
}

#search-menu .results a {
  margin-top: 1%;
  margin-bottom: 1%;
  display: block;
  cursor: pointer;
  text-decoration: none;
  color: white;
  font-family: "ABeeZee", sans-serif;
  font-size: 0.85vw;
}

.network-search {
  margin-left: 3%;
}

.result-label {
  margin-left: 3%;
  width: 93%;
  font-family: "ABeeZee", sans-serif;
  color: rgba(255, 255, 255, 50%);
  font-size: 0.73vw;
  border-bottom: 1px solid;
  border-color: rgba(255, 255, 255, 50%);
  cursor: default;
}

.google-search {
  display: flex;
  width: 100%;
  height: 100%;
  align-items: center;
}

.google-search a {
  margin-left: 1%;
}

.google-logo {
  margin-left: 3%;
  height: 0.8vw;
  width: 0.8vw;
}

.check-active {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 998;
}

.search-background {
  position: fixed;
  width: 25%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 998;
  -webkit-backdrop-filter: blur(4vw);
}
</style>
