<template>
  <Button severity="secondary" type="button" label="Export protein graph data" icon="pi pi-download" iconPos="right"
    class="!w-full !justify-between !rounded-lg" @click="toggle" />
  <Popover class="w-[13rem]" ref="op" :pt="{ content: { class: 'px-1 flex flex-col gap-1' } }">
    <ExportGraph></ExportGraph>
    <ExportProteins :gephi_data="gephi_data"></ExportProteins>
    <ExportEdges :gephi_data="gephi_data" :ensembl_name_index="ensembl_name_index"></ExportEdges>
  </Popover>
</template>

<script setup>
import { ref } from "vue";

const op = ref();

const toggle = (event) => {
  op.value.toggle(event);
};
</script>

<script>
import ExportProteins from "@/components/toolbar/modules/ExportProteins.vue";
import ExportEdges from "@/components/toolbar/modules/ExportEdges.vue";
import ExportGraph from "@/components/toolbar/modules/ExportGraph.vue";
export default {
  name: "ExportGraphData",
  props: ["mode", "gephi_data", "ensembl_name_index"],
  components: {
    ExportProteins,
    ExportEdges,
    ExportGraph
  },
  data() {
    return {};
  },
};
</script>
