<template>
  <div class="slider" tabindex="0">
    <span v-if="citation_graphs.size == 0"
      >There is no generated citation graph.</span
    >
    <div
      v-for="(entry, index) in filt_graphs"
      :key="index"
      class="graph"
      v-on:click="switch_graph(entry)"
      @mouseover="activeGraphIndex = index"
      @mouseout="activeGraphIndex = -1"
    >
      <SnapshotCitation :propValue="entry" :index="entry.id" />
      <div class="graph-options">
        <div
          class="bookmark-graph"
          v-show="activeGraphIndex == index"
          v-on:click.stop="add_graph(entry)"
          :class="{ checked: favourite_graphs.has(entry.id) }"
          ref="checkboxStatesGraph"
        ></div>
        <img
          class="remove-graph"
          v-show="activeGraphIndex == index"
          src="@/assets/pathwaybar/cross.png"
          v-on:click.stop="remove_graph(entry)"
        />
        <div class="graph-citation-name">
          <input type="text" v-model="entry.label" class="empty" @click.stop />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SnapshotCitation from "@/components/citation/SnapshotCitation.vue";

export default {
  name: "CitationGraphs",
  props: ["citation_graphs", "favourite_graphs", "bookmark_off", "mode"],
  emits: ["favourite_graph_changed"],
  components: {
    SnapshotCitation,
  },
  data() {
    return {
      activeGraphIndex: -1,
    };
  },
  methods: {
    switch_graph(entry) {
      this.$store.commit("assign_citation_graph", {
        id: entry.id,
        graph: entry.graph,
      });
      this.$router.push("citation");
    },
    remove_graph(entry) {
      if (!this.favourite_graphs.has(entry.id)) {
        // Checkbox is checked, add its state to the object
        this.favourite_graphs.delete(entry.id);
      }
      this.citation_graphs.delete(entry);
      this.$store.commit("remove_snapshotCitation", entry.id);
      this.$store.commit("remove_citation_graph", entry);
      if (
        ![...this.citation_graphs].some(
          (e) => e.id == this.$store.state.citation_graph_data.id
        )
      ) {
        this.$store.commit("assign_citation_graph", null);
      }
    },
    add_graph(entry) {
      if (!this.favourite_graphs.has(entry.id)) {
        this.favourite_graphs.add(entry.id);
      } else {
        this.favourite_graphs.delete(entry.id);
      }
    },
  },
  computed: {
    filt_graphs() {
      var com = this;
      var filtered = [...com.citation_graphs];

      if (!com.bookmark_off) {
        filtered = filtered.filter(function (abstract) {
          return com.favourite_graphs.has(abstract.id);
        });
      }

      return new Set(filtered);
    },
  },
};
</script>

<style>
.graph-citation-name {
  position: fixed;
  display: flex;
  bottom: 5%;
  width: 100%;
  height: 20%;
  -webkit-backdrop-filter: blur(7.5px);
  text-align-last: center;
  justify-content: center;
}

.graph-citation-name input[type="text"] {
  font-size: 0.5vw;
  background: none;
  color: white;
  cursor: default;
  font-family: "ABeeZee", sans-serif;
  border: none;
}
</style>
