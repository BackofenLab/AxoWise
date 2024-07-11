<template>
  <img :id="'heatmap-visual-' + index" />
</template>

<script>
import heatmapDendro from "@/components/enrichment/heatmap/drawHeatmap";

export default {
  props: ["propValue", "index"],
  data() {
    return {
      snapshot: null,
    };
  },
  updated() {
    if (this.findSnapshot())
      this.initializeSnapshot(this.findSnapshot().snapshot);
  },
  mounted() {
    if (!this.findSnapshot())
      this.initializeSnapshot(this.getSnapshot(this.propValue.graph));
    else this.initializeSnapshot(this.findSnapshot().snapshot);
  },
  methods: {
    findSnapshot() {
      return this.$store.state.snapshot_heatmaps.find(
        (dictionary) => dictionary.id === this.index
      );
    },
    initializeSnapshot(data) {
      const imageContainer = document.getElementById(
        "heatmap-visual-" + this.index
      );
      imageContainer.src = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(
        data
      )}`;
    },
    getSnapshot(data) {
      var image = heatmapDendro(data, "#sigma-heatmap", true);
      this.$store.commit("assign_snapshotHeatmap", {
        id: this.index,
        snapshot: image,
      });

      return image;
    },
  },
};
</script>

<style>
[id^="heatmap-visual-"] {
  height: 100%;
  width: 100%;
  overflow: scroll;
  object-fit: scale-down;
  border: solid 0.05vw rgba(255, 255, 255, 0.3);
}
</style>
