<template>
  <header
    class="flex items-center sticky top-0 gap-2 py-3 bg-[var(--card-bg)] shadow-curve-dark dark:shadow-curve-light z-[1]">
    <h5 class="mb-0 mr-auto">List of Heatmap ({{ favourite_graphs.length || 0 }})</h5>

    <Button severity="secondary" rounded size="small" plain class="w-8 h-8" v-on:click="get_svg()"
      v-tooltip.bottom="'Download heatmap'">
      <span class="text-2xl material-symbols-rounded"> download </span>
    </Button>

    <Button severity="secondary" rounded size="small" plain v-on:click="bookmark_off = !bookmark_off" class="w-8 h-8"
      v-tooltip.bottom="bookmark_off ? 'Show all' : 'Show favorites'">
      <span :class="`material-symbols-rounded text-2xl
          ${bookmark_off ? '' : 'font-variation-ico-filled text-yellow-500 hover:text-yellow-400'}`">
        star
      </span>
    </Button>

    <Button severity="secondary" label="Generate heatmap" icon="pi pi-plus" size="small" v-on:click="get_heatmap()" />
  </header>

  <PathwayHeatmap :bookmark_off="bookmark_off"></PathwayHeatmap>

  <!-- <div id="heatmap-graphs">
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
  </div> -->
</template>

<script>
import PathwayHeatmap from "@/components/enrichment/heatmap/PathwayHeatmap.vue";

export default {
  name: "HeatmapTool",
  props: ["gephi_data", "filtered_terms", "favourite_pathways", "mode"],
  components: {
    PathwayHeatmap,
  },
  data() {
    return {
      favourite_graphs: new Set(),
      bookmark_off: true,
      // tool_selecting: false
    };
  },
  methods: {
    get_heatmap() {
      if (this.favourite_pathways.length == 0) {
        // FIXME: Use toast instead of alert
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

<!-- <style>
#heatmap-graphs {
  width: 100%;
  height: 100%;
  z-index: 999;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: "ABeeZee", sans-serif;
}
</style> -->
