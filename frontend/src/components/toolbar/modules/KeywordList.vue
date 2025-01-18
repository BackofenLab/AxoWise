<template>
  <InputGroup>
    <InputText v-model="search_raw" placeholder="Search by keywords..." />
    <InputGroupAddon class="!p-0">
      <Button icon="material-symbols-rounded" text plain
        v-tooltip.bottom="{ value: 'Select all keywords', pt: { text: '!text-sm' } }"
        @click="search_subset(filt_keyword)">
        <span class="material-symbols-rounded">arrow_forward_ios</span>
      </Button>
    </InputGroupAddon>
  </InputGroup>

  <ul class="max-h-[200px] flex flex-wrap gap-2 mt-5 pr-2 overflow-auto">
    <li v-for="(entry, index) in filt_keyword" v-on:click="select_node(entry)" :key="index" :class="`${mode === 'term' ? 'w-[calc((100%-(10px*2))/2)] text-left' : 'w-[calc((100%-(10px*2))/3)] text-center '} px-2 py-1.5 border rounded-md text-sm font-semibold cursor-pointer
      ${active_genes.has(entry.label)
        ? 'border-primary-400 bg-primary-400/10'
        : 'border-slate-300'
      }`">
      {{ entry.attributes["Name"] }}
    </li>
  </ul>

  <h6 v-if="search_raw.length >= 2 && filt_keyword.length === 0" class="text-center text-slate-300">
    No available data
  </h6>

  <Button v-if="filt_keyword.length !== 0" label="Create subset" severity="secondary" size="small" fluid type="button"
    class="mt-4 !rounded-lg" @click="save_subset()">
  </Button>
</template>

<script>
import { useToast } from "primevue/usetoast";

export default {
  name: "KeywordList",
  props: ["gephi_data", "mode"],
  data() {
    return {
      search_raw: "",
      active_genes: new Set(),
    };
  },
  mounted() {
    this.toast = useToast();
  },
  methods: {
    select_node(node) {
      if (node)
        this.emitter.emit("searchNode", { node: node, mode: this.mode });
    },
    search_subset(subset) {
      var com = this;
      com.emitter.emit("searchSubset", { subset: subset, mode: this.mode });
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
      this.toast.add({ severity: 'success', detail: 'Subset created successfully.', life: 4000 });
    },
  },
  computed: {
    regex() {
      var com = this;
      return RegExp(
        com.search_raw.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
      );
    },
    filt_keyword() {
      var com = this;
      var matches = [];

      if (com.search_raw.length >= 2) {
        com.active_genes = com.$store.state.active_subset
          ? new Set(com.$store.state.active_subset)
          : new Set();
        var regex = new RegExp(com.regex, "i");
        matches = com.gephi_data.nodes.filter(function (node) {
          return (
            regex.test(node.attributes["Description"]) || regex.test(node.label)
          );
        });
      }
      return matches;
    },
  },
};
</script>
