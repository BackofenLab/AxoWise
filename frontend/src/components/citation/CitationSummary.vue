<template>
  <ListActionHeader :title="`Please separate each abstracts with comma (,)`">
    <Button severity="secondary" rounded size="small" plain class="w-8 h-8" v-on:click="raw_text = ''; summary = ''"
      v-tooltip.bottom="'Reset'">
      <span class="text-2xl material-symbols-rounded"> refresh </span>
    </Button>
    <InputGroup>
      <IconField class="w-full">
        <InputText v-model="raw_text" placeholder="Enter abstracts..." class="w-full" />
      </IconField>

      <InputGroupAddon>
        <Button severity="secondary" @click="summarize_abstracts(raw_text, false)" label="Apply" text plain
          :loading="await_load" />
      </InputGroupAddon>
    </InputGroup>
  </ListActionHeader>

  <EmptyState v-if="!await_load && !summary" message="There is no generated summary.">
  </EmptyState>

  <div v-if="await_load" class="flex flex-col items-center justify-center h-full gap-3">
    <h6 class="flex items-center gap-2 dark:text-slate-300">Fetching summary
      <span class="relative flex">
        <span class="absolute inline-flex w-full h-full rounded-full opacity-75 animate-ping bg-primary-500"></span>
        <span
          class="material-symbols-rounded text-primary-500 animate animate-[spin_1s_ease-in-out_infinite]">scatter_plot</span>
      </span>
    </h6>
  </div>

  <div v-if="!await_load && summary" class="mt-3 whitespace-pre-wrap">
    {{ summary }}
  </div>
</template>

<script>
import ListActionHeader from "@/components/verticalpane/ListActionHeader.vue";
import EmptyState from "@/components/verticalpane/EmptyState.vue";
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
  components: {
    ListActionHeader,
    EmptyState
  },
  methods: {
    add_abstract(id) {
      // This doesn't seem user friendly instead use ','
      // this.raw_text = this.raw_text + `${this.raw_text.length != 0 ? "\n" : ""}` + id;
      this.raw_text = this.raw_text + `${this.raw_text.length != 0 ? "," : ""}` + id;
    },
    add_subset(subset) {
      for (var node of subset) {
        // this.raw_text = this.raw_text + `${this.raw_text.length != 0 ? "\n" : ""}` + node.id;
        this.raw_text = this.raw_text + `${this.raw_text.length != 0 ? "," : ""}` + node.id;
      }
    },
    summarize_abstracts(abstracts, community_check) {
      var com = this;

      com.finalList = [];
      if (community_check == false) {
        com.await_load = true;
        var abstractList = {};
        // for (var node of abstracts.split("\n")) {
        for (var node of abstracts.split(",").map(item => item.trim())) {
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

      const contextD = com.$store.state.context_dict;
      var formData = new FormData();
      formData.append("abstracts", JSON.stringify(com.finalList));
      formData.append("base", contextD.base);
      formData.append("context", contextD.context);
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