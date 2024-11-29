<template>
  <ListActionHeader>
    <IconField class="flex-1">
      <InputText v-model="search_raw" placeholder="Search in sets" class="w-full" />
      <InputIcon class="z-10 pi pi-search" />
    </IconField>

    <Button class="flex-shrink-0" severity="primary" label="Add subset" icon="pi pi-plus" size="small" raised
      v-on:click="save_subset()" />
    <!-- <Button class="flex-shrink-0" severity="primary" label="Add subset" icon="pi pi-plus" size="small" raised
      @click="toggle" /> -->

    <div class="grid w-full grid-cols-12 gap-x-2">
      <a class="flex items-center justify-start col-span-4 gap-1 cursor-pointer" v-on:click="
        sort_alph = sort_alph === 'asc' ? 'dsc' : 'asc';
      sort_pr = '';
      sort_cb = '';
      sort_y = '';
      ">
        Subset

        <span :class="`material-symbols-rounded text-base cursor-pointer 
            ${sort_alph ? 'text-primary-500' : 'text-slate-600'}`">
          {{ !sort_alph ? "swap_vert" : sort_alph === "asc" ? "south" : "north" }}
        </span>
      </a>

      <label class="flex items-center justify-start col-span-2">Nodes</label>

      <label class="flex items-center justify-start col-span-3">View</label>

      <label class="col-span-4"></label>
    </div>
  </ListActionHeader>

  <Panel v-for="(entry, index) in filt_abstracts" class="!bg-transparent !border-0 mb-1.5" :collapsed="true" toggleable
    :key="index" :pt="{
      header: { class: 'relative !p-0 !rounded hover:bg-slate-300/50 dark:hover:bg-slate-700/50' },
      content: { class: '!p-3 !rounded-b-lg bg-slate-200 dark:bg-slate-800' },
      headerActions: { class: 'absolute right-0' },
    }">
    <template #header>
      <div
        class="w-full grid grid-cols-12 items-center gap-2 !py-0 !px-0 !font-normal !text-slate-500 dark:!text-slate-300 !leading-tight">
        <label class="relative col-span-4">
          <span :class="`w-full h-full flex items-center gap-2 border border-transparent hover:border-slate-500/50 dark:hover:border-slate-300/50 rounded absolute top-0 left-0 py-2 px-1 text-sm font-medium cursor-text z-[1]
              ${focus_subset_id === index ? '!hidden' : ''}`" v-on:click="setFocus(entry.id, index)">
            {{ entry.name }} <span class="text-lg material-symbols-rounded dark:text-slate-200"> edit </span>
          </span>
          <input ref="subsetInputs" type="text" v-model="entry.name" :class="`w-full border rounded border-primary-400 bg-transparent py-2 px-1 text-sm font-medium ${focus_subset_id === index ? '' : 'opacity-0'
            }`" @click.stop @blur="clearFocus" />
        </label>

        <label class="col-span-2">{{ entry.genes.length }}</label>

        <label class="col-span-2 capitalize">{{ entry.view }}</label>

        <label class="col-span-4 flex gap-1.5">
          <Button severity="secondary" rounded size="small" text plain v-on:click.stop="set_active(entry)"
            v-tooltip.bottom="'View on graph'" class="w-6 h-6 !text-slate-500 dark:!text-slate-300">
            <i :class="`material-symbols-rounded text-xl
            ${entry.status ? 'font-variation-ico-filled text-primary-500 hover:text-primary-400' : ''}`">
              graph_3
            </i>
          </Button>

          <Button severity="danger" size="small" rounded text v-on:click.stop="remove_set(entry)"
            v-tooltip.bottom="'Remove selection'" class="w-6 h-6 !text-slate-500 dark:!text-slate-300">
            <i class="text-xl material-symbols-rounded"> delete </i>
          </Button>

          <Button severity="danger" size="small" rounded text v-on:click.stop="addToChatbot(entry)"
            v-tooltip.bottom="'Chat with Axo bot'" class="w-6 h-6 !text-slate-500 dark:!text-slate-300">
            <span class="text-xl material-symbols-rounded"> forum </span>
          </Button>
        </label>
      </div>
    </template>

    <div class="grid grid-cols-5 gap-3">
      <span class="text-sm text-center capitalize" v-for="element in entry.stats" :key="element">{{ element }}</span>
    </div>

    <Button v-if="!entry.stats" severity="contrast" label="Apply enrichment" icon="pi pi-plus" size="small" raised fluid
      :loading="loading_state" @click="apply_enrichment(entry)" />
  </Panel>

  <EmptyState v-if="filt_abstracts.size === 0" message="There is no generated subsets">
  </EmptyState>

  <!-- <Popover ref="op" class="w-[15rem]" :pt="{ content: { class: '!flex !flex-col' } }">
    <Button text plain severity="secondary" type="button" label="Import from selected subset"
      class="!justify-start !py-1" />
    <Button text plain severity="secondary" type="button" label="By searching in genes"
      class="!justify-start !py-1" />
    <Button text plain severity="secondary" type="button" label="By searching in keywords"
      class="!justify-start !py-1" />
    <Button text plain severity="secondary" type="button" label="By parameter filtering"
      class="!justify-start !py-1" />
  </Popover> -->
  `<!-- <div id="pathways-set">
    <div class="tool-set-section-graph">
      <div class="coloumn-set-button">
        <button class="tool-buttons" v-on:click="save_subset()">
          <img class="buttons-img" src="@/assets/plus-1.png" />
        </button>
      </div>
      <div class="citation-search">
        <img class="citation-search-icon" src="@/assets/toolbar/search.png" />
        <input type="text" v-model="search_raw" class="empty" placeholder="search in sets" />
      </div>
    </div>
    <div class="list-section">
      <div class="sorting">
        <a class="pubid_filter" v-on:click="
          sort_alph = sort_alph === 'asc' ? 'dsc' : 'asc';
        sort_pr = '';
        sort_cb = '';
        sort_y = '';
        ">subset</a>
        <a class="nodes_filter">nodes</a>
        <a class="view_filter">view</a>
      </div>

      <div class="results" tabindex="0" @keydown="handleKeyDown" ref="resultsContainer">
        <table>
          <tbody>
            <span v-for="(entry, index) in filt_abstracts" :key="index">
              <tr class="set-table">
                <td>
                  <div class="favourite-symbol" v-on:click="set_active(entry)">
                    <label class="custom-checkbox">
                      <div class="active-image" :class="{ checked: entry.status }"></div>
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
                    <div class="functions-image" v-on:click="entry.information = !entry.information"></div>
                  </label>
                  <label class="custom-icons" v-if="entry.view == 'protein'">
                    <div class="expand-image" v-on:click="entry.actions = !entry.actions"></div>
                  </label>
                </td>
                <td>
                  <label class="custom-icons">
                    <div class="delete-image" v-on:click="remove_set(entry)"></div>
                  </label>
                  <label class="custom-icons">
                    <div class="chatbot-image" v-on:click="addToChatbot(entry)"></div>
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
                  <button class="tool-buttons" v-on:click="apply_enrichment(entry)">
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
  </div> -->
</template>`

<!-- <script setup>
import { ref } from "vue";

const op = ref();

const toggle = (event) => {
  op.value.toggle(event);
};
</script> -->

<script>
import ListActionHeader from "@/components/ListActionHeader.vue";
import { nextTick } from "vue";

export default {
  name: "PathwaySet",
  props: ["gephi_data", "api", "mode"],
  components: {
    ListActionHeader,
  },
  emits: ["term_set_changed"],
  data() {
    return {
      set_dict: new Set(),
      search_raw: "",
      layer: 0,
      loading_state: false,
      focus_subset_id: null
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
        console.log(filtered);
      }

      return new Set(filtered);
    },
  },
  methods: {
    setFocus(id, index) {
      this.focus_subset_id = index;

      nextTick(() => {
        // Focus the input if focus_subset_id matches the current id
        const input = this.$refs.subsetInputs[index];
        if (input) {
          input.focus();
        }
      });
    },
    clearFocus() {
      this.focus_subset_id = null;
    },
    apply_enrichment(subset) {
      var com = this;

      if (!subset.genes || com.loading_state) {
        alert("please select a subset or pathway to apply enrichment");
        return;
      }

      //Adding proteins and species to formdata
      var formData = new FormData();
      formData.append("genes", subset.genes);
      formData.append("species_id", com.gephi_data.nodes[0].species);
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
        data: this.activate_genes(subset.genes, subset.view),
      });
    },
    save_subset() {
      var com = this;
      let genes;
      if (com.mode == "protein") {
        genes = com.$store.state.active_subset;
      } else if (com.mode == "term") {
        genes = com.$store.state.p_active_subset;
      } else {
        genes = com.$store.state.c_active_subset;
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
      for (var layer of this.$store.state.favourite_subsets) {
        if (layer != entry) layer.status = false;
      }

      this.$router.push(entry.view).then(() => {
        if (!entry.status) {
          this.emitter.emit("searchSubset", {
            subset: this.activate_genes(entry.genes, entry.view),
            mode: entry.view,
          });
          this.emitter.emit("enrichTerms", entry.terms);
        } else {
          this.emitter.emit("searchSubset", { subset: null, mode: entry.view });
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

<!-- <style>
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
  overflow: hidden;
  /* Hide overflow content */
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
</style> -->
