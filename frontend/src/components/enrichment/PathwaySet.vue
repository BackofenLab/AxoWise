<template>
  <ListActionHeader>
    <IconField class="flex-1">
      <InputText v-model="search_raw" placeholder="Search in sets" class="w-full" />
      <InputIcon class="z-10 pi pi-search" />
    </IconField>

    <SplitButton class="flex-shrink-0" label="Add subset" severity="primary" icon="pi pi-plus" size="small" raised
      @click="save_subset" :model="subset_options" />

    <div class="grid w-full grid-cols-12 gap-x-2">
      <a class="flex items-center justify-start col-span-4 gap-1 cursor-pointer" v-on:click="
        sort_alph = sort_alph === 'asc' ? 'dsc' : 'asc';
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

  <Panel v-for="(entry, index) in filt_abstracts" class="!bg-transparent !border-0 mb-1.5" :collapsed="true"
    :toggleable="entry.view == 'protein'" :key="index" :pt="{
      header: { class: 'relative !p-0 !rounded hover:bg-slate-300/50 dark:hover:bg-slate-700/50' },
      content: { class: '!p-3 !rounded-b-lg bg-slate-200 dark:bg-slate-800' },
      headerActions: { class: 'absolute right-0' },
    }">
    <template #header>
      <div
        class="w-full h-full grid grid-cols-12 items-center gap-2 !py-0 !px-0 !font-normal !text-slate-500 dark:!text-slate-300 !leading-tight">
        <label class="relative col-span-4">
          <span :class="`w-full h-full flex items-center absolute top-0 left-0 gap-2 border border-transparent hover:border-slate-500/50 dark:hover:border-slate-300/50 rounded py-2 px-1 text-sm font-medium cursor-text z-[1]
              ${focus_subset_id === index ? '!hidden' : ''}`" v-on:click="setFocus(entry.id, index)">
            <span class="max-w-[calc(100%-24px)] line-clamp-1">{{ entry.name }}</span> <span
              class="text-lg material-symbols-rounded dark:text-slate-200"> edit </span></span>
          <input ref="subsetInputs" type="text" v-model="entry.name" :class="`w-full h-full border rounded border-primary-400 bg-transparent py-2 px-1 text-sm font-medium ${focus_subset_id === index ? '' : 'opacity-0'
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
            v-tooltip.bottom="'Remove subset'" class="w-6 h-6 !text-slate-500 dark:!text-slate-300">
            <i class="text-xl material-symbols-rounded"> delete </i>
          </Button>

          <Button severity="danger" size="small" rounded text v-on:click.stop="addToChatbot(entry)"
            v-tooltip.bottom="'Add to chatbot'" class="w-6 h-6 !text-slate-500 dark:!text-slate-300">
            <span class="text-xl material-symbols-rounded"> forum </span>
          </Button>
        </label>
      </div>
    </template>

    <div class="grid grid-cols-5 gap-3">
      <span class="text-sm text-center capitalize" v-for="element in entry.stats" :key="element">
        {{ element?.split(":")?.[0] }} <br />
        {{ element?.split(":")?.[1] }}
      </span>
    </div>

    <Button v-if="!entry.stats" severity="contrast" label="Apply enrichment" icon="pi pi-plus" size="small" raised fluid
      :loading="loading_state" @click="apply_enrichment(entry)" />
  </Panel>

  <EmptyState v-if="filt_abstracts.size === 0" message="There is no generated subsets.">
  </EmptyState>

  <Dialog v-model:visible="keyword_active" header="Highlight nodes" position="topleft" :minY="60" :minX="60" :pt="{
    root: { class: 'w-[24rem] !mt-[60px] !ml-[60px]' },
    header: { class: '!py-2.5 cursor-move' },
    title: { class: '!text-base' },
  }">
    <KeywordList v-show="keyword_active" :gephi_data="gephi_data" :mode="mode">
    </KeywordList>
  </Dialog>

  <Dialog v-model:visible="selection_active" header="Graph parameter" position="topleft" :minY="60" :minX="60" :pt="{
      root: { class: 'w-[25rem] !mt-[60px] !ml-[60px]' },
      header: { class: '!py-2.5 cursor-move' },
      title: { class: '!text-base' },
    }">
      <SelectionList :data="gephi_data" :selection_active="selection_active" :active_subset="null"
        :active_term="null" :mode="mode">
      </SelectionList>
    </Dialog>

    <Dialog v-model:visible="protein_active" header="Highlight nodes" position="topleft" :minY="60" :minX="60" :pt="{
      root: { class: 'w-[24rem] !mt-[60px] !ml-[60px]' },
      header: { class: '!py-2.5 cursor-move' },
      title: { class: '!text-base' },
    }">
      <ProteinList v-show="protein_active" :gephi_data="gephi_data" :mode="mode">
      </ProteinList>
    </Dialog>
</template>

<script>
import ListActionHeader from "@/components/verticalpane/ListActionHeader.vue";
import ProteinList from "@/components/toolbar/modules/ProteinList.vue";
import SelectionList from "@/components/toolbar/modules/SelectionList.vue";
import KeywordList from "@/components/toolbar/modules/KeywordList.vue";
import EmptyState from "@/components/verticalpane/EmptyState.vue";
import { useToast } from "primevue/usetoast";
import { nextTick } from "vue";

export default {
  name: "PathwaySet",
  props: ["gephi_data", "api", "mode"],
  components: {
    ListActionHeader,
    EmptyState,
    ProteinList,
    SelectionList,
    KeywordList
  },
  emits: ["term_set_changed"],
  data() {
    return {
      sort_alph: "",
      set_dict: new Set(),
      search_raw: "",
      loading_state: false,
      focus_subset_id: null,
      keyword_active: false,
      protein_active: false,
      selection_active: false,
      subset_options: [
        {
          label: 'By searching in genes',
          command: () => {
            this.protein_active = !this.protein_active
          }
        },
        {
          label: 'By searching in keywords',
          command: () => {
            this.keyword_active = !this.keyword_active
          }
        },
        {
          label: 'By parameter filtering',
          command: () => {
            this.selection_active = !this.selection_active
          }
        },
      ]
    };
  },
  mounted() {
    this.toast = useToast();
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

      if (com.sort_alph == "asc") {
        filtered.sort(function (t1, t2) {
          return t1.name.toLowerCase() > t2.name.toLowerCase()
            ? 1
            : t1.name.toLowerCase() === t2.name.toLowerCase()
              ? 0
              : -1;
        });
      } else if (com.sort_alph == "dsc") {
        filtered.sort(function (t1, t2) {
          return t2.name.toLowerCase() > t1.name.toLowerCase()
            ? 1
            : t1.name.toLowerCase() === t2.name.toLowerCase()
              ? 0
              : -1;
        });
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
        this.toast.add({ severity: 'error', detail: 'Please select a subset or pathway to apply enrichment.', life: 4000 });
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
      let count = new Set(com.$store.state.favourite_subsets)?.size || 0;
      if (com.mode == "protein") {
        genes = com.$store.state.active_subset;
      } else if (com.mode == "term") {
        genes = com.$store.state.p_active_subset;
      } else {
        genes = com.$store.state.c_active_subset;
      }

      if (!genes) return;

      this.$store.commit("assign_subset", {
        name: `subset ${count}`,
        genes: genes,
        terms: null,
        view: com.mode,
        abstracts: null,
        status: false,
        information: false,
        actions: false,
        stats: null,
      });
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