<template>
  <img class="object-cover w-full h-full" :id="'graph-visual-' + index" />
</template>

<script>
import saveAsSVG from "../../../rendering/saveAsSVG";

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
  activated() {
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
      return this.$store.state.snapshot_pathways.find(
        (dictionary) => dictionary.id === this.index
      );
    },
    initializeSnapshot(data) {
      const imageContainer = document.getElementById(
        "graph-visual-" + this.index
      );
      imageContainer.src = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(
        data
      )}`;
    },
    getSnapshot(data) {
      var sigma_instance = new sigma();
      var camera = sigma_instance.addCamera();

      sigma_instance.addRenderer({
        container: "graph-visual-" + this.index,
        type: "canvas",
        camera: camera,
        settings: {
          defaultLabelColor: "#FFF",
          hideEdgesOnMove: true,
          minNodeSize: 1,
          maxNodeSize: 20,
          labelThreshold: 5,
        },
      });

      sigma_instance.graph.clear();
      sigma_instance.graph.read(data);

      var image = saveAsSVG(sigma_instance, {
        download: false,
        width: 200,
        height: 200,
      });
      this.$store.commit("assign_snapshotPathway", {
        id: this.index,
        snapshot: image,
      });

      sigma_instance.kill();

      return image;
    },
  },
};
</script>
