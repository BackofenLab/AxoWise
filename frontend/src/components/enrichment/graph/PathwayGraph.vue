<template>
  <EmptyState v-if="term_graphs.size == 0" message="There is no generated enrichment graph">
  </EmptyState>

  <!-- <div class="loading-section">
    <div class="loading-text" v-if="term_graphs.size == 0">
      <span>There is no generated pathway graph.</span>
    </div>
    <div class="slider" tabindex="0" v-if="term_graphs.size != 0">
      <div v-for="(entry, index) in filt_graphs" :key="index" class="graph" v-on:click="switch_graph(entry)"
        @mouseover="activeGraphIndex = index" @mouseout="activeGraphIndex = -1">
        <SnapshotGraph :propValue="entry" :index="entry.id" />
        <div class="graph-options">
          <div class="bookmark-graph" v-show="activeGraphIndex == index" v-on:click.stop="add_graph(entry)"
            :class="{ checked: favourite_graphs.has(entry.id) }" ref="checkboxStatesGraph"></div>
          <img class="remove-graph" v-show="activeGraphIndex == index" src="@/assets/pathwaybar/cross.png"
            v-on:click.stop="remove_graph(entry)" />
          <div class="graph-name">
            <input type="text" v-model="entry.label" class="empty" @click.stop />
          </div>
        </div>
      </div>
    </div>
  </div> -->

  <section v-if="term_graphs.size != 0" class="grid grid-cols-2 gap-2.5 pt-3">
    <Card v-for="(entry, index) in filt_graphs" :class="`group relative overflow-hidden border ${active_enrichment_id === entry.id
      ? 'border-primary-600 !bg-primary-600/25'
      : 'dark:!bg-slate-300/25 border-transparent'
      }`" :key="index" :pt="{
        header: { class: 'h-30 relative rounded-md mt-[6px] mx-[6px] overflow-hidden' },
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
        <h6 :class="`w-full h-full flex items-center gap-2 absolute top-0 left-0 py-2 px-2 text-sm font-medium cursor-text z-[1]
          ${focus_enrichment_id === entry.id ? '!hidden' : ''}`" v-on:click="setFocus(entry.id, index)">
          {{ entry.label }} <span class="text-lg material-symbols-rounded dark:text-slate-200"> edit </span>
        </h6>
        <input ref="enrichmentInputs" type="text" v-model="entry.label"
          :class="`bg-transparent py-2 px-2 text-sm font-medium ${focus_enrichment_id === entry.id ? '' : 'opacity-0'}`"
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
      // activeGraphIndex: -1,
      graph_number: -1,
      // species: null,
      focus_enrichment_id: null,
      active_enrichment_id: null
    };
  },
  mounted() {
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
          com.$emit("loading_state_changed", false);
        }
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

<!-- <style>
.graph-section .slider {
  width: 100%;
  max-height: 100%;
  display: flex;
  padding: 0.5vw 1vw 0.5vw 1vw;
  flex-wrap: wrap;
  overflow-y: scroll;
  scroll-behavior: smooth;
  scroll-snap-type: x mandatory;
}

/* Hide scrollbar for Chrome, Safari and Opera */
.graph-section .slider::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.graph-section .slider {
  -ms-overflow-style: none;
  /* IE and Edge */
  scrollbar-width: none;
  /* Firefox */
}

.graph-section .slider .graph {
  position: relative;
  width: 33%;
  height: 7.5vw;
  padding: 0.5vw;
  flex-shrink: 0;
  transform-origin: center center;
  transform: scale(1);
  scroll-snap-align: center;
  display: flex;
}

.graph-section .slider .graph:hover {
  background: rgba(217, 217, 217, 0.12);
}

.bookmark-graph {
  display: block;
  width: 0.9vw;
  height: 0.9vw;
  margin: 1% 1% 0 0;
  background-color: rgba(255, 255, 255, 0.62);
  -webkit-mask: url(@/assets/pathwaybar/star-solid.svg) no-repeat center;
  mask: url(@/assets/pathwaybar/star-solid.svg) no-repeat center;
  mask-size: 0.9vw;
  background-repeat: no-repeat;
}

.remove-graph {
  width: 0.9vw;
  height: 0.9vw;
  -webkit-filter: invert(100%);
  /* Safari/Chrome */
  filter: invert(100%);
  margin: 1% 1% 0 0;
}

.graph-options {
  position: absolute;
  width: 100%;
  padding: 0 0.5vw 0 0.5vw;
  display: flex;
  align-items: center;
  justify-content: end;
}

.graph-name {
  position: fixed;
  display: flex;
  bottom: 5%;
  width: 100%;
  height: 20%;
  -webkit-backdrop-filter: blur(7.5px);
  text-align-last: center;
  justify-content: center;
}

.graph-name input[type="text"] {
  font-size: 0.85vw;
  background: none;
  color: white;
  cursor: default;
  font-family: "ABeeZee", sans-serif;
  border: none;
  padding: 0 0.5vw 0 0.5vw;
  overflow: hidden;
}

.checked {
  background-color: #ffa500;
}

.slider span {
  width: 100%;
  height: 100%;
  text-align: center;
  color: white;
  font-size: 0.7vw;
}

.loading-section {
  height: 100%;
  width: 100%;
  padding: 0.5vw;
  border: solid 0.01vw rgba(255, 255, 255, 0.5);
}

.loading-text {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.7vw;
}
</style> -->
