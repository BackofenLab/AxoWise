<template>
  <ListActionHeader :title="`List of citation graph`">
    <Button severity="secondary" rounded size="small" plain v-on:click="bookmark_off = !bookmark_off" class="w-8 h-8"
      v-tooltip.bottom="bookmark_off ? 'Show only favorites' : 'Show all'">
      <span :class="`material-symbols-rounded text-2xl
          ${bookmark_off ? '' : 'font-variation-ico-filled text-yellow-500 hover:text-yellow-400'}`">
        star
      </span>
    </Button>

    <Button severity="secondary" label="Generate citation" icon="pi pi-plus" size="small" :loading="loading_state"
      v-on:click="get_citation_graph(context_raw)" />
  </ListActionHeader>

  <CitationGraph :citation_graphs="citation_graphs" :favourite_graphs="favourite_graphs" :bookmark_off="bookmark_off"
    @loading_state_changed="loading_state = $event" @favourite_graphs_changed="favourite_graphs = $event">
  </CitationGraph>
</template>

<script>
import CitationGraph from "@/components/citation/CitationGraph.vue";
import ListActionHeader from "@/components/verticalpane/ListActionHeader.vue";

export default {
  name: "CitationMenu",
  props: ["active_node", "active_background"],
  components: {
    CitationGraph,
    ListActionHeader
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
