<template>
  <div id="heatmap-graphs">
    <div class="tool-section-graph">
      <div class="coloumn-button">
        <button class="tool-buttons" v-on:click="get_heatmap()">
          <img class="buttons-img" src="@/assets/plus-1.png" />
        </button>
      </div>
      <div class="coloumn-button">
        <button
          class="tool-buttons"
          :class="{ recolor_filter: bookmark_off == false }"
          v-on:click="bookmark_off = !bookmark_off"
        >
          <img class="buttons-img" src="@/assets/star.png" />
        </button>
      </div>
      <div class="coloumn-button">
        <button class="tool-buttons" v-on:click="get_svg()">
          <img class="buttons-img" src="@/assets/toolbar/download.png" />
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
      if (this.favourite_pathways.length == 0) {
        alert("favorize pathways before generating heatmap");
        return;
      }
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
