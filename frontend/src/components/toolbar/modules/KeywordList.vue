<template>
  <InputGroup>
    <InputText v-model="search_raw" placeholder="Search by keywords..." />
    <InputGroupAddon class="!p-0">
      <Button icon="material-symbols-rounded" text plain v-tooltip.bottom="'Search subset'"
        @click="search_subset(filt_keyword)">
        <span class="material-symbols-rounded">arrow_forward_ios</span>
      </Button>
    </InputGroupAddon>
  </InputGroup>

  <ul class="max-h-[200px] flex flex-wrap gap-2 mt-5 pr-2 overflow-auto">
    <li v-for="(entry, index) in filt_keyword" v-on:click="select_node(entry)" :key="index" :class="`w-[calc((100%-(10px*2))/3)] px-2 py-1.5 border rounded-md text-sm text-center font-semibold cursor-pointer
      ${active_genes.has(entry.label)
        ? 'border-primary-400 bg-primary-400/10'
        : 'border-slate-300'
      }`">
      {{ entry.attributes["Name"] }}
    </li>
  </ul>

  <h6 v-if="filt_keyword.length === 0" class="text-center text-slate-300">
    No available data
  </h6>
</template>

<script>
export default {
  name: "KeywordList",
  props: ["gephi_data", "mode"],
  data() {
    return {
      search_raw: "",
      active_genes: new Set(),
    };
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
