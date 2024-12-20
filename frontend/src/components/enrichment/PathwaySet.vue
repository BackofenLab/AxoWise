<template>
  <div id="pathways-set">
    <div class="tool-set-section-graph">
      <div class="coloumn-set-button">
        <button class="tool-buttons" v-on:click="save_subset()">
          <img class="buttons-img" src="@/assets/plus-1.png" />
        </button>
      </div>
      <div class="citation-search">
        <img class="citation-search-icon" src="@/assets/toolbar/search.png" />
        <input
          type="text"
          v-model="search_raw"
          class="empty"
          placeholder="search in sets"
        />
      </div>
    </div>
    <div class="list-section">
      <div class="sorting">
        <a
          class="pubid_filter"
          v-on:click="
            sort_alph = sort_alph === 'asc' ? 'dsc' : 'asc';
            sort_pr = '';
            sort_cb = '';
            sort_y = '';
          "
          >subset</a
        >
        <a class="nodes_filter">nodes</a>
        <a class="view_filter">view</a>
      </div>

      <div
        class="results"
        tabindex="0"
        @keydown="handleKeyDown"
        ref="resultsContainer"
      >
        <table>
          <tbody>
            <span v-for="(entry, index) in filt_abstracts" :key="index">
              <tr class="set-table">
                <td>
                  <div class="favourite-symbol" v-on:click="set_active(entry)">
                    <label class="custom-checkbox">
                      <div
                        class="active-image"
                        :class="{ checked: entry.status }"
                      ></div>
                    </label>
                  </div>
                </td>
                <td>
                  <div class="pathway-text">
                    <input type="text" v-model="entry.name" class="empty" />
                  </div>
                </td>
                <td>
                  <div class="pathway-text">
                    <span>({{ entry.genes.length }})</span>
                  </div>
                </td>
                <td>
                  <div class="pathway-text">
                    <span>{{ entry.view }}</span>
                  </div>
                </td>
                <td>
                  <label class="custom-icons" v-if="entry.view == 'protein'">
                    <div
                      class="functions-image"
                      v-on:click="entry.information = !entry.information"
                    ></div>
                  </label>
                  <label class="custom-icons" v-if="entry.view == 'protein'">
                    <div
                      class="expand-image"
                      v-on:click="entry.actions = !entry.actions"
                    ></div>
                  </label>
                </td>
                <td>
                  <label class="custom-icons">
                    <div
                      class="delete-image"
                      v-on:click="remove_set(entry)"
                    ></div>
                  </label>
                  <label class="custom-icons">
                    <div
                      class="chatbot-image"
                      v-on:click="addToChatbot(entry)"
                    ></div>
                  </label>
                </td>
              </tr>
              <tr v-if="entry.information" class="expanded">
                <td v-for="element in entry.stats" :key="element">
                  <div class="information-set">{{ element }}</div>
                </td>
              </tr>
              <tr v-if="entry.actions" class="expanded">
                <div class="actions-tab">
                  <button
                    class="tool-buttons"
                    v-on:click="apply_enrichment(entry)"
                  >
                    <img class="buttons-img" src="@/assets/plus-1.png" />
                    <div v-if="loading_state" class="loading_button"></div>
                  </button>
                  <span> apply enrichment {{ entry.enriched }} </span>
                </div>
              </tr>
            </span>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { useVisualizationStore } from "@/store/ProteinStore";

export default {
  name: "PathwaySet",
  props: ["gephi_data", "api", "mode"],
  emits: ["term_set_changed"],
  setup(){
    const store = useVisualizationStore();
    return { store };
  },
  data() {
    return {
      set_dict: new Set(),
      search_raw: "",
      layer: 0,
      loading_state: false,
    };
  },
  computed: {
    regex() {
      var com = this;
      return RegExp(
        com.search_raw.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
      );
    },
    filt_abstracts() {
      var com = this;
      var filtered = [...this.$store.state.favourite_subsets];

      if (com.search_raw !== "") {
        // If search term is not empty, filter by search term
        var regex = new RegExp(com.regex, "i");
        filtered = filtered.filter(function (set) {
          if (set.stats != null) {
            return regex.test(set.stats.join(" ")) || regex.test(set.name);
          } else {
            return regex.test(set.name);
          }
        });
      }

      return new Set(filtered);
    },
  },
  methods: {
    apply_enrichment(subset) {
      var com = this;

      if (!subset.genes || com.loading_state) {
        alert("please select a subset or pathway to apply enrichment");
        return;
      }

      const symbolList = com.gephi_data.nodes
      .filter((node) => subset.genes.has(node.ENSEMBL_PROTEIN))
      .map((node) => node.label);

      //Adding proteins and species to formdata
      var formData = new FormData();
      formData.append("genes", symbolList);
      formData.append("species_id", com.gephi_data.settings.species);
      formData.append(
        "mapping",
        JSON.stringify(com.gephi_data.settings["gene_alias_mapping"])
      );

      com.loading_state = true;
      //POST request for generating pathways
      com.sourceToken = this.axios.CancelToken.source();
      com.axios
        .post(com.api.subgraph, formData, {
          cancelToken: com.sourceToken.token,
        })
        .then((response) => {
          subset.terms = response.data.sort(
            (t1, t2) => t1.fdr_rate - t2.fdr_rate
          );
          console.log(response.data)
          subset.stats = com.get_significant_words(response.data);
          subset.name = subset.name + " (e)";
          com.loading_state = false;
          subset.actions = false;
        });
    },
    addToChatbot(subset) {
      this.emitter.emit("addToChatbot", {
        id: `${subset.view}:${subset.name}`,
        mode: subset.view,
        type: "subset",
        data: subset.genes
      });
    },
    save_subset() {
      var com = this;
      const { store } = this;
      let genes;
      if (com.mode == "protein") {
        genes = store.clickedCluster;
      } else if (com.mode == "term") {
        genes = store.clickedCluster;
      } else {
        genes = store.clickedCluster;
      }

      if (!genes) return;

      this.$store.commit("assign_subset", {
        name: `subset ${com.layer}`,
        genes: genes,
        terms: null,
        view: com.mode,
        abstracts: null,
        status: false,
        information: false,
        actions: false,
        stats: null,
      });
      com.layer += 1;
    },
    remove_set(entry) {
      if (entry.status) this.emitter.emit("enrichTerms", null);
      this.set_dict.delete(entry);
      this.$store.commit("delete_subset", entry);
    },
    set_active(entry) {
      const { store } = this;
      for (var layer of this.$store.state.favourite_subsets) {
        if (layer != entry) layer.status = false;
      }

      this.$router.push(entry.view).then(() => {
        if (!entry.status) {
          store.setClickedSubset(entry.genes)
          this.emitter.emit("enrichTerms", entry.terms);
        } else {
          store.setClickedSubset(new Set())
          this.emitter.emit("enrichTerms", null);
        }
        entry.status = !entry.status;
      });
    },
    activate_genes(genes, view) {
      var subset = [];
      var genes_set = new Set(genes);
      let data;

      if (view === "citation") {
        data = this.$store.state.citation_graph_data.graph;
      } else if (view === "term") {
        data = this.$store.state.term_graph_data.graph;
      } else if (view === "protein") {
        data = this.$store.state.gephi_json.data;
      }

      console.log(data)

      data.nodes.forEach((node) => {
        if (genes_set.has(node.attributes["Name"])) {
          subset.push(node);
        }
      });

      return subset;
    },
    get_significant_words(term_set) {
      const namesArray = term_set.map((obj) => obj.name);
      const text = namesArray.join(", ");

      if (text == null) return null;

      const topWords = this.getTopWords(text);

      return topWords;
    },
    getTopWords(text) {
      const stopwords = new Set([
        "i",
        "me",
        "my",
        "myself",
        "we",
        "our",
        "ours",
        "ourselves",
        "you",
        "your",
        "yours",
        "yourself",
        "yourselves",
        "he",
        "him",
        "his",
        "himself",
        "she",
        "her",
        "hers",
        "herself",
        "it",
        "its",
        "itself",
        "they",
        "them",
        "their",
        "theirs",
        "themselves",
        "what",
        "which",
        "who",
        "whom",
        "this",
        "that",
        "these",
        "those",
        "am",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "having",
        "do",
        "does",
        "did",
        "doing",
        "a",
        "an",
        "the",
        "and",
        "but",
        "if",
        "or",
        "because",
        "as",
        "until",
        "while",
        "of",
        "at",
        "by",
        "for",
        "with",
        "about",
        "against",
        "between",
        "into",
        "through",
        "during",
        "before",
        "after",
        "above",
        "below",
        "to",
        "from",
        "up",
        "down",
        "in",
        "out",
        "on",
        "off",
        "over",
        "under",
        "again",
        "further",
        "then",
        "once",
        "here",
        "there",
        "when",
        "where",
        "why",
        "how",
        "all",
        "any",
        "both",
        "each",
        "few",
        "more",
        "most",
        "other",
        "some",
        "such",
        "no",
        "nor",
        "not",
        "only",
        "own",
        "same",
        "so",
        "than",
        "too",
        "very",
        "s",
        "t",
        "can",
        "will",
        "just",
        "don",
        "should",
        "now",
      ]);

      // Step 1: Tokenize the text and filter out stopwords
      const words = text
        .toLowerCase()
        .match(/\b\w+\b/g)
        .filter((word) => !stopwords.has(word));

      // Step 2: Count word frequencies
      const wordCount = {};
      words.forEach((word) => {
        if (wordCount[word]) {
          wordCount[word]++;
        } else {
          wordCount[word] = 1;
        }
      });

      // Step 3: Calculate percentages
      const totalWords = words.length;
      const wordPercentages = {};
      Object.keys(wordCount).forEach((word) => {
        const percentage = (wordCount[word] / totalWords) * 100;
        wordPercentages[word] = percentage.toFixed(2); // Limiting to 2 decimal places
      });

      // Step 4: Sort words by frequency and select top 10
      const sortedWords = Object.keys(wordPercentages)
        .sort((a, b) => wordCount[b] - wordCount[a])
        .slice(0, 5);

      // Step 5: Prepare and return results
      const topWordsWithPercentages = sortedWords.map(
        (word) => `${word}: ${wordPercentages[word]}%`
      );
      return topWordsWithPercentages;
    },
  },
};
</script>

<style>
#pathways-set {
  width: 100%;
  height: 100%;
  cursor: default;
  font-family: "ABeeZee", sans-serif;
}

.pathway-apply-section {
  width: 100%;
  height: 87.65%;
  border-radius: 5px;
  position: absolute;
}

.generate-set-button {
  display: inline-flex;
  margin: 1vw 0 1vw 0;
  height: 1vw;
  width: 100%;
  padding: 0 2vw 0 2vw;
}

.generate-set-button .export-text {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0a0a1a;
  font-size: 0.7vw;
}

.pathway-apply-section a {
  color: white;
  text-decoration: none;
}

.pathway-apply-section .results {
  height: 100%;
  overflow: scroll;
}
.pathway-apply-section .sorting a {
  color: rgba(255, 255, 255, 0.7);
}

.set-table {
  display: -webkit-flex;
  padding-top: 0.4vw;
}

#pathways-set .pathway-text {
  width: 80%;
  display: flex;
  align-items: center;
  white-space: nowrap;
  overflow: hidden; /* Hide overflow content */
  text-overflow: ellipsis;
  margin-left: 2%;
}

.nodes_filter {
  position: absolute;
  left: 35%;
}
.view_filter {
  position: absolute;
  left: 50%;
}

#pathways-set .pathway-text input[type="text"] {
  width: 100%;
  font-size: 0.85vw;
  background: none;
  color: white;
  cursor: default;
  font-family: "ABeeZee", sans-serif;
  border: none;
}
#pathways-set .pathway-text span {
  font-size: 0.7vw;
  margin-left: 4%;
  color: rgba(255, 255, 255, 0.7);
}

#pathways-set .pathway-text a {
  cursor: default;
}

/* bookmark styles */

table {
  display: flex;
  width: 100%;
}

:focus {
  outline: 0 !important;
}

table tbody {
  width: 100%;
}
.set-table td:first-child {
  width: 3.41%;
  align-self: center;
}
.set-table td:nth-child(2) {
  color: #fff;
  font-size: 0.9vw;
  width: 30%;
  padding: 0 0 0 2px;
  overflow: hidden;
  align-self: center;
}
.set-table td:nth-child(3) {
  color: #fff;
  font-size: 0.9vw;
  width: 15%;
  padding: 0 0 0 2px;
  overflow: hidden;
  align-self: center;
}
.set-table td:nth-child(4) {
  color: #fff;
  font-size: 0.9vw;
  width: 23%;
  padding: 0 0 0 2px;
  overflow: hidden;
  align-self: center;
}
.set-table td:nth-child(5) {
  font-size: 0.7vw;
  color: white;
  width: 13%;
  align-self: center;
}
.set-table td:last-child {
  font-size: 0.7vw;
  color: white;
  width: 13%;
  align-self: center;
}

.favourite-symbol {
  width: 100%;
  height: 100%;
  justify-content: center;
  text-align: center;
  position: relative;
  display: flex;
}
.custom-checkbox {
  position: relative;
  display: inline-block;
  cursor: default;
}

.checked {
  background-color: #ffa500;
}

.expanded td:first-child,
.expanded td:nth-child(2),
.expanded td:nth-child(3),
.expanded td:nth-child(4),
.expanded td:last-child {
  color: #fff;
  width: 20%;
  overflow: hidden;
  align-self: center;
}

.custom-icons {
  position: relative;
  display: inline-block;
  cursor: default;
  padding-right: 0.5vw;
}

.active-image {
  display: block;
  width: 0.9vw;
  height: 0.9vw;
  background-color: white;
  -webkit-mask: url(@/assets/pathwaybar/star-solid.svg) no-repeat center;
  mask: url(@/assets/pathwaybar/star-solid.svg) no-repeat center;
  mask-size: 0.9vw;
  background-repeat: no-repeat;
}

.delete-image {
  display: block;
  width: 0.9vw;
  height: 0.9vw;
  background-color: white;
  -webkit-mask: url(@/assets/pathwaybar/delete.png) no-repeat center;
  mask: url(@/assets/pathwaybar/delete.png) no-repeat center;
  mask-size: 0.9vw;
  background-repeat: no-repeat;
}

.expand-image {
  display: block;
  width: 0.9vw;
  height: 0.9vw;
  background-color: white;
  -webkit-mask: url(@/assets/toolbar/menu-burger.png) no-repeat center;
  mask: url(@/assets/toolbar/menu-burger.png) no-repeat center;
  mask-size: 0.9vw;
  background-repeat: no-repeat;
}

.functions-image {
  display: block;
  width: 0.9vw;
  height: 0.9vw;
  background-color: white;
  -webkit-mask: url(@/assets/toolbar/settings-sliders.png) no-repeat center;
  mask: url(@/assets/toolbar/settings-sliders.png) no-repeat center;
  mask-size: 0.9vw;
  background-repeat: no-repeat;
}

.chatbot-image {
  display: block;
  width: 0.9vw;
  height: 0.9vw;
  background-color: white;
  -webkit-mask: url(@/assets/toolbar/bote.png) no-repeat center;
  mask: url(@/assets/toolbar/bote.png) no-repeat center;
  mask-size: 0.9vw;
  background-repeat: no-repeat;
}

.checked {
  background-color: #ffa500;
}

.selected {
  background-color: rgba(255, 0, 0, 0.7);
}

.tool-set-section-graph {
  display: grid;
  grid-template-columns: 0.5fr 0.5fr;
  padding: 1vw 1vw 1vw 1vw;
  width: 100%;
  flex-shrink: 0;
}

.coloumn-set-button {
  padding-right: 0.5vw;
  display: grid;
  row-gap: 1vw;
  z-index: 9999;
}

.information-set {
  font-size: 0.5vw;
  display: flex;
  justify-content: center;
  text-align: center;
  padding: 0.2vw;
}
.actions-tab {
  font-size: 0.5vw;
  display: flex;
  justify-content: center;
  text-align: center;
  padding: 0.2vw;
  color: white;
}

.expanded {
  display: -webkit-flex;
  padding: 0 2vw 0 2vw;
  background: rgba(255, 255, 255, 0.1);
  background-clip: content-box;
}

.actions-tab span {
  align-self: center;
  margin-left: 0.2rem;
}
.actions-tab .loading-button {
  position: absolute;
}

.actions-tab .tool-buttons {
  padding: 0.2vw 0.2vw 0.2vw 0.2vw;
  border-radius: 0;
  cursor: pointer;
  display: flex;
  font-size: 0.7vw;
  align-items: center;
  color: rgba(255, 255, 255, 0.8);
  justify-content: center;
  border: 0.05vw solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 2px 6px -3px rgba(255, 255, 255, 0.23);
  transition: transform 0.25s cubic-bezier(0.7, 0.98, 0.86, 0.98),
    box-shadow 0.25s cubic-bezier(0.7, 0.98, 0.86, 0.98);
  background-color: #0a0a1a;
}
</style>
