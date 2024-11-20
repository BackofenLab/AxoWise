<template>
  <div id="citation-tools" class="pathways">
    <div class="pathwaybar">
      <div id="citation-graphs">
        <div class="tool-section-graph">
          <div class="coloumn-button">
            <button class="tool-buttons" v-on:click="get_citation_graph(context_raw)">
              <img class="buttons-img" src="@/assets/plus-1.png" v-if="!loading_state" />
              <div v-if="loading_state" class="loading_button"></div>
            </button>
          </div>
          <div class="coloumn-button">
            <button class="tool-buttons" :class="{ recolor_filter: bookmark_off == false }"
              v-on:click="bookmark_off = !bookmark_off">
              <img class="buttons-img" src="@/assets/star.png" />
            </button>
          </div>
        </div>
        <div class="graph-section">
          <CitationGraph :citation_graphs="citation_graphs" :favourite_graphs="favourite_graphs"
            :bookmark_off="bookmark_off" @loading_state_changed="loading_state = $event"
            @favourite_graphs_changed="favourite_graphs = $event"></CitationGraph>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CitationGraph from "@/components/citation/CitationGraph.vue";

export default {
  name: "CitationMenu",
  props: ["active_node", "active_background"],
  components: {
    CitationGraph,
  },
  data() {
    return {
      citation_graphs: [],
      citation_graphs_array: [],
      favourite_graphs: new Set(),
      graph_number: -1,
      bookmark_off: true,
      loading_state: false,
      api: {
        context: "api/subgraph/context",
      },
      context_raw: "",
    };
  },
  mounted() {
    this.citation_graphs_array = this.$store.state.citation_graph_dict;
    if (this.citation_graphs_array.length != 0) {
      this.graph_number = Math.max.apply(
        Math,
        this.citation_graphs_array.map((item) => item.id)
      );
      this.citation_graphs = new Set(this.citation_graphs_array);
    } else {
      this.citation_graphs = new Set();
    }
  },
  deactivated() {
    this.$store.commit("assign_citation_dict", [...this.citation_graphs]);
  },
  activated() {
    this.citation_graphs = new Set(this.$store.state.citation_graph_dict);
  },
  methods: {
    get_citation_graph(context) {
      var com = this;

      if (com.loading_state) return;

      com.loading_state = true;
      const [year, citations] = [true, true];
      var base = this.active_background || "";
      com.getContext(base, context, com.get_rank(year, citations));
    },
    get_rank(year, citations) {
      return year && citations
        ? "all"
        : year
          ? "year"
          : citations
            ? "citations"
            : "all";
    },
    getContext(base, context, rank) {
      var com = this;

      var background;

      if (Object.keys(base)[0] == "Protein") {
        background = base["Protein"].value.attributes["Name"];
      } else if (Object.keys(base)[0] == "Subset") {
        background = base["Subset"].value.map((node) => node.label).join(" ");
      } else if (Object.keys(base)[0] == "Pathway") {
        background = base["Pathway"].value.symbols.join(" ");
      } else {
        background = "";
      }

      //Adding proteins and species to formdata
      var formData = new FormData();
      formData.append("base", background);
      formData.append("context", context);
      formData.append("rank", rank);

      this.$store.commit("assign_context_br", {
        base: background,
        context: context,
      });

      //POST request for generating pathways
      com.axios.post(com.api.context, formData).then((response) => {
        if (response.data.length != 0) {
          this.graph_number += 1;
          if (this.citation_graphs.size < 1) {
            this.$store.commit("assign_citation_graph", {
              id: this.graph_number,
              graph: response.data,
            });
          }
          this.$store.commit("assign_new_citation_graph", {
            id: this.graph_number,
            label: `Graph ${this.graph_number}`,
            graph: response.data,
          });
          this.citation_graphs.add({
            id: this.graph_number,
            label: `Graph ${this.graph_number}`,
            graph: response.data,
          });
        }
        com.loading_state = false;
      });
    },
    change_citation() {
      this.$router.push("citation");
    },
  },
};
</script>

<style>
#citation-graphs {
  width: 100%;
  height: 100%;
  z-index: 999;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: "ABeeZee", sans-serif;
}

.citation-search {
  background: rgba(222, 222, 222, 0.3);
  padding: 0 0 0 0.3vw;
  height: 1.4vw;
  display: flex;
  align-items: center;
  align-content: center;
  justify-content: center;
}

.citation-search-icon {
  margin-left: 3%;
  position: relative;
  height: 0.9vw;
  width: 0.9vw;
  filter: invert(100%);
}

.citation-search input[type="text"] {
  margin-left: 0.5vw;
  width: 16vw;
  font-size: 0.85vw;
  background: none;
  color: white;
  cursor: default;
  border: none;
  font-family: "ABeeZee", sans-serif;
}

.citation-search [type="text"]::-webkit-input-placeholder {
  opacity: 70%;
}

.context-check {
  margin-top: 0.2vw;
  margin-bottom: 0.2vw;
}

.context-confirm {
  font-family: "ABeeZee", sans-serif;
  color: white;
  font-size: 0.7vw;
  display: flex;
}

.context-confirm [type="checkbox"]+label {
  display: block;
  cursor: pointer;
  font-family: sans-serif;
  font-size: 24px;
  line-height: 1.3;
  position: absolute;
  left: 7vw;
  margin-top: 0.7%;
}

.context-confirm [type="checkbox"]+label:before {
  width: 1.2vw;
  height: 0.6vw;
  border-radius: 30px;
  background-color: #ddd;
  content: "";
  transition: background-color 0.5s linear;
  z-index: 5;
  position: absolute;
}

.context-confirm [type="checkbox"]+label:after {
  width: 0.4vw;
  height: 0.4vw;
  border-radius: 30px;
  background-color: #fff;
  content: "";
  transition: margin 0.1s linear;
  box-shadow: 0px 0px 5px #aaa;
  position: absolute;
  top: 10%;
  margin: 0.09vw 0 0 0.09vw;
  z-index: 10;
}

.context-confirm [type="checkbox"]:checked+label:after {
  margin: 0.09vw 0 0 0.69vw;
}

.loading_pane_citation {
  content: "";
  position: absolute;
  width: 1vw;
  height: 1vw;
  border: 4px solid transparent;
  border-top-color: #ffffff;
  border-radius: 50%;
  right: 1vw;
  animation: button-loading-spinner 1s ease infinite;
}
</style>
