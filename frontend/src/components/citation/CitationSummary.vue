<template>
  <div id="citation-tools" class="pathways">
    <div class="pathwaybar">
      <div class="summary-input">
        <div class="window-label">gene search</div>
        <textarea v-model="raw_text" rows="10" cols="30" autofocus></textarea>
        <button v-on:click="summarize_abstracts(raw_text, false)">apply</button>
      </div>
      <div class="summarized">
        <div class="window-label">summary</div>
        <div class="summarized-abstracts">
          <div v-if="await_load == true" class="loading_pane"></div>
          <div class="text" v-if="await_load == false">
            {{ summary }}
          </div>
        </div>
      </div>
    </div>
    <!-- <div class="summary-pop" v-if="community_check == true"> Text of Example</div> -->
  </div>
</template>

<script>
export default {
  name: "CitationSummary",
  props: ["active_function", "sorted", "citation_data", "node_index"],
  emits: ["await_community_changed"],
  data() {
    return {
      raw_text: "",
      summary: "",
      api: {
        summary: "api/subgraph/summary",
      },
      abstractList: null,
      await_load: false,
      finalList: null,
      savedOverview: {},
      graphID: null,
    };
  },
  methods: {
    add_abstract(id) {
      this.raw_text =
        this.raw_text + `${this.raw_text.length != 0 ? "\n" : ""}` + id;
    },
    add_subset(subset) {
      for (var node of subset) {
        this.raw_text =
          this.raw_text + `${this.raw_text.length != 0 ? "\n" : ""}` + node.id;
      }
    },
    summarize_abstracts(abstracts, community_check) {
      var com = this;

      com.finalList = [];
      if (community_check == false) {
        com.await_load = true;
        var abstractList = {};
        for (var node of abstracts.split("\n")) {
          if (com.node_index[node]) abstractList[node] = com.node_index[node];
        }
        com.finalList.push(abstractList);
      } else {
        this.$emit("await_community_changed", true);
        for (var community of abstracts) {
          var communityAbstract = {};
          for (var nodes of community) {
            if (com.node_index[nodes.id])
              communityAbstract[nodes.id] = com.node_index[nodes.id];
          }
          com.finalList.push(communityAbstract);
        }
      }

      var formData = new FormData();
      formData.append("abstracts", JSON.stringify(com.finalList));
      formData.append("community_check", community_check);

      //POST request for generating pathways
      com.axios.post(com.api.summary, formData).then((response) => {
        if (community_check) {
          com.savedOverview[com.graphID] = response.data.replace(/\\n/g, "\n");
          alert(response.data.replace(/\\n/g, "\n"));
          this.$emit("await_community_changed", false);
        } else {
          com.summary = response.data.replace(/\\n/g, "\n");
          com.await_load = false;
        }
      });
    },
  },
  mounted() {
    var com = this;
    com.graphID = com.$store.state.citation_graph_data.id;
    this.emitter.on("addNodeToSummary", (id) => {
      this.add_abstract(id);
    });
    this.emitter.on("addSubsetToSummary", (subset) => {
      this.add_subset(subset);
    });
    this.emitter.on("generateSummary", (subset) => {
      if (com.savedOverview[com.graphID] == undefined)
        com.summarize_abstracts(subset, true);
      else alert(com.savedOverview[com.graphID]);
    });
  },
  activated() {
    this.graphID = this.$store.state.citation_graph_data.id;
  },
};
</script>

<style>
.summary-input {
  position: relative;
  padding: 1vw;
  width: 100%;
  height: 30%;
}
.summary-input textarea {
  margin-top: 3%;
  font-size: 0.9vw;
  width: 100%;
  color: white;
  background-color: rgba(255, 255, 255, 0.05);
  text-align: center;
  border: none;
  padding-top: 5%;
  resize: none;
  outline: none;
  height: 100%;
}
.summarized {
  position: relative;
  padding: 1vw;
  width: 100%;
  height: 70%;
}
.summarized-abstracts {
  color: white;
  font-family: "ABeeZee", sans-serif;
  background-color: rgba(255, 255, 255, 0.05);
  font-size: 0.7vw;
  width: 100%;
  height: 90%;
  margin-top: 3%;
  overflow-y: scroll;
  padding: 1.3vw 1.3vw 0 1.3vw;
}
.summary-input button {
  position: absolute;
  right: 2vw;
  top: 0.8vw;
  position: absolute;
  display: block;
  cursor: pointer;
  border: none;
  color: white;
  border-style: solid;
  border-width: 1px;
  background: #0a0a1a;
  border-color: white;
  width: 3vw;
  font-size: 0.7vw;
}

.text {
  white-space: pre-wrap; /* This will render whitespace and line breaks */
}
</style>
