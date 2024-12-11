<template>
  <ListActionHeader :title="`List of Heatmap`">
    <Button severity="secondary" rounded size="small" plain class="w-8 h-8" v-on:click="get_svg()"
      v-tooltip.bottom="'Download heatmap'">
      <span class="text-2xl material-symbols-rounded"> download </span>
    </Button>

    <Button severity="secondary" rounded size="small" plain v-on:click="bookmark_off = !bookmark_off" class="w-8 h-8"
      v-tooltip.bottom="bookmark_off ? 'Show only favorites' : 'Show all'">
      <span :class="`material-symbols-rounded text-2xl
          ${bookmark_off ? '' : 'font-variation-ico-filled text-yellow-500 hover:text-yellow-400'}`">
        star
      </span>
    </Button>
    
    <Button severity="secondary" label="Generate heatmap" icon="pi pi-plus" size="small" v-on:click="get_heatmap()" />
  </ListActionHeader>

  <PathwayHeatmap :bookmark_off="bookmark_off"></PathwayHeatmap>
</template>

<script>
import PathwayHeatmap from "@/components/enrichment/heatmap/PathwayHeatmap.vue";
import ListActionHeader from "@/components/verticalpane/ListActionHeader.vue";
import { useToast } from "primevue/usetoast";

export default {
  name: "HeatmapTool",
  props: ["gephi_data", "filtered_terms", "favourite_pathways", "mode"],
  components: {
    PathwayHeatmap,
    ListActionHeader
  },
  data() {
    return {
      bookmark_off: true,
    };
  },
  mounted() {
    this.toast = useToast();
  },
  methods: {
    get_heatmap() {
      if (this.favourite_pathways.length == 0) {
        this.toast.add({ severity: 'error', detail: 'Please favorize pathways before generating heatmap.', life: 4000 });
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
