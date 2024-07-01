<template>
  <div id="heatmap-graphs">
    <div class="tool-section-graph">
      <div class="coloumn-button">
        <button class="tool-buttons" v-on:click="get_heatmap()">
          generate heatmap
        </button>
      </div>
      <div class="coloumn-button">
        <button class="tool-buttons" v-on:click="get_svg()">
          export snapshot
        </button>
      </div>
    </div>
    <div class="graph-section">
      <PathwayHeatmap :bookmark_off="bookmark_off"></PathwayHeatmap>
    </div>
  </div>
</template>

<script>
import PathwayHeatmap from "@/components/enrichment/heatmap/PathwayHeatmap.vue";

export default {
  name: "HeatmapTool",
  props: ["gephi_data", "filtered_terms", "favourite_pathways"],
  components: {
    PathwayHeatmap,
  },
  data() {
    return {
      favourite_graphs: new Set(),
      bookmark_off: true,
      tool_selecting: false,
      mode: "protein",
    };
  },
  methods: {
    get_heatmap() {
      this.emitter.emit("generateHeatmap", this.favourite_pathways);
    },
    get_svg() {
      this.emitter.emit("exportHeatmap");
    },
  },
};
</script>

<style>
#heatmap-graphs {
  width: 100%;
  height: 100%;
  z-index: 999;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: "ABeeZee", sans-serif;
}
</style>
