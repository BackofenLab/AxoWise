<template>
  <ListActionHeader :title="`Please enter each abstracts in a new line.`">
    <Button severity="secondary" rounded size="small" plain class="w-8 h-8" v-on:click="raw_text = ''; summary = ''"
      v-tooltip.bottom="'Reset'">
      <span class="text-2xl material-symbols-rounded"> refresh </span>
    </Button>
  </ListActionHeader>

  <Textarea v-model="raw_text" rows="3" fluid autofocus class="w-full text-center" />
  <Button label="Apply" severity="secondary" size="small" fluid type="button" class="mt-2.5 !rounded-lg"
    @click="summarize_abstracts(raw_text, false)" :loading="await_load">
  </Button>

  <EmptyState v-if="!await_load && !summary" message="There is no generated summary.">
  </EmptyState>

  <p v-if="!await_load && summary" class="mt-3 text-md text-primary-400">Generated Summary:</p>
  
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