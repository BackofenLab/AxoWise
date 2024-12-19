<template>
  <EmptyState v-if="term_graphs.size == 0" message="There is no generated enrichment graph.">
  </EmptyState>

  <section v-if="term_graphs.size != 0" class="grid grid-cols-2 gap-2.5 pt-3">
    <Card v-for="(entry, index) in filt_graphs" :class="`group relative overflow-hidden border ${active_enrichment_id === entry.id
      ? 'border-primary-600 !bg-primary-600/25'
      : 'dark:!bg-slate-300/25 !bg-slate-300/10 border-transparent'
      }`" :key="index" :pt="{
        header: { class: 'h-[138px] relative rounded-md mt-[6px] mx-[6px] overflow-hidden' },
        body: { class: '!p-0 !gap-0' },
        footer: { class: 'flex gap-2 px-2 pb-2' },
        title: { class: 'relative' },
      }">
      <template #header>
        <SnapshotGraph :propValue="entry" :index="entry.id" />

        <div
          class="w-full h-full flex justify-between absolute top-0 left-0 p-1.5 bg-slate-800/50 opacity-0 duration-300 group-hover:opacity-100 z-[1]">
          <Button class="w-7 h-7" severity="secondary" rounded size="small" plain @click.stop="add_graph(entry)">
            <span :class="`material-symbols-rounded  ${favourite_graphs.has(entry.id)
              ? 'text-base font-variation-ico-filled text-yellow-500 hover:text-yellow-400'
              : 'text-xl hover:text-yellow-600'
              }`">
              star
            </span>
          </Button>

          <Button class="w-7 h-7" severity="danger" rounded size="small" plain @click.stop="remove_graph(entry)">
            <span class="text-xl text-white material-symbols-rounded"> close </span>
          </Button>
        </div>
      </template>

      <template #title>
        <h6 :class="`w-full  h-full absolute top-0 left-0 flex items-center gap-2 py-2 px-2 text-sm font-medium cursor-text z-[1]
          ${focus_enrichment_id === entry.id ? '!hidden' : ''}`" v-on:click="setFocus(entry.id, index)">
          <span class="max-w-[calc(100%-24px)] line-clamp-1">{{ entry.label }}</span> <span
            class="text-lg material-symbols-rounded dark:text-slate-200"> edit </span>
        </h6>
        <input ref="enrichmentInputs" type="text" v-model="entry.label"
          :class="`w-full bg-transparent py-2 px-2 text-sm font-medium ${focus_enrichment_id === entry.id ? '' : 'opacity-0'}`"
          @click.stop @blur="clearFocus" />
      </template>

      <template #footer>
        <Button class="flex-1 h-8" severity="secondary" size="small" plain @click="switch_graph(entry)">
          View <span class="text-xl material-symbols-rounded"> arrow_circle_right </span>
        </Button>
      </template>
    </Card>
  </section>
</template>

<script>
import SnapshotGraph from "@/components/enrichment/graph/SnapshotGraph.vue";
import EmptyState from "@/components/verticalpane/EmptyState.vue";
import { nextTick } from "vue";
import { useToast } from "primevue/usetoast";

export default {
  name: "PathwayGraphs",
  props: ["gephi_data", "filtered_terms", "bookmark_off", "mode"],
  emits: ["loading_state_changed"],
  components: {
    SnapshotGraph,
    EmptyState
  },
  data() {
    return {
      api: {
        termgraph: "api/subgraph/terms",
      },
      term_graphs: [],
      term_graphs_array: [],
      favourite_graphs: new Set(),
      graph_number: -1,
      focus_enrichment_id: null,
      active_enrichment_id: null
    };
  },
  mounted() {
    this.toast = useToast();
    if (this.mode != "term") {
      this.emitter.on("generateGraph", (set) => {
        this.get_term_data(set);
      });
    }
    this.term_graphs_array = this.$store.state.term_graph_dict;
    this.favourite_graphs = this.$store.state.favourite_graph_dict;
    if (this.term_graphs_array.length != 0) {
      this.graph_number = Math.max.apply(
        Math,
        this.term_graphs_array.map((item) => item.id)
      );
      this.term_graphs = new Set(this.term_graphs_array);
    } else {
      this.term_graphs = new Set();
    }
  },
  deactivated() {
    this.$store.commit("assign_term_dict", [...this.term_graphs]);
  },
  beforeUnmount() {
    this.emitter.off("generateGraph");
  },
  activated() {
    this.term_graphs = new Set(this.$store.state.term_graph_dict);
    this.favourite_graphs = this.$store.state.favourite_graph_dict;
  },
  methods: {
    setFocus(id, index) {
      this.focus_enrichment_id = id;
      nextTick(() => {
        // Focus the input if focus_enrichment_id matches the current id
        const input = this.$refs.enrichmentInputs[index];
        if (input) {
          input.focus();
        }
      });
    },
    clearFocus() {
      this.focus_enrichment_id = null;
    },
    get_term_data(set) {
      var com = this;

      var formData = new FormData();
      if (!set)
        formData.append("func-terms", JSON.stringify(com.filtered_terms));
      else formData.append("func-terms", JSON.stringify(set));
      formData.append("species_id", com.gephi_data.nodes[0].species);

      this.axios.post(com.api.termgraph, formData).then((response) => {
        if (response.data) {
          this.graph_number += 1;
          if (this.term_graphs.size < 1) {
            this.$store.commit("assign_term_graph", {
              id: this.graph_number,
              graph: response.data,
            });
          }
          this.$store.commit("assign_new_term_graph", {
            id: this.graph_number,
            label: `Graph ${this.graph_number}`,
            graph: response.data,
          });
          this.term_graphs.add({
            id: this.graph_number,
            label: `Graph ${this.graph_number}`,
            graph: response.data,
          });
          this.toast.add({ severity: 'success', detail: 'Enrichment graph created successfully.', life: 4000 });
        } else {
          this.toast.add({ severity: 'error', detail: 'Unable to create enrichment graph. Please try again later.', life: 4000 });
        }
        com.$emit("loading_state_changed", false);
      });
    },
    switch_graph(entry) {
      this.active_enrichment_id = entry.id;
      this.$store.commit("assign_term_graph", {
        id: entry.id,
        graph: entry.graph,
      });
      if (this.mode == "term") this.emitter.emit("graphChanged");
      else this.$router.push("term");
    },
    remove_graph(entry) {
      if (!this.favourite_graphs.has(entry.id)) {
        // Checkbox is checked, add its state to the object
        this.favourite_graphs.delete(entry.id);
      }
      this.term_graphs.delete(entry);
      this.$store.commit("remove_term_graph", entry);

      if (this.$store.state.term_graph_data == null) return;

      if (
        ![...this.term_graphs].some(
          (e) => e.id == this.$store.state.term_graph_data.id
        )
      ) {
        this.$store.commit("assign_term_graph", null);
      }
    },
    add_graph(entry) {
      if (!this.favourite_graphs.has(entry.id)) {
        this.favourite_graphs.add(entry.id);
      } else {
        this.favourite_graphs.delete(entry.id);
      }
      this.$store.commit("assign_favourite_graph", this.favourite_graphs);
    },
  },
  computed: {
    filt_graphs() {
      var com = this;
      var filtered = [...com.term_graphs];

      if (!com.bookmark_off) {
        filtered = filtered.filter(function (term) {
          return com.favourite_graphs.has(term.id);
        });
      }

      return new Set(filtered);
    },
  },
};
</script>
