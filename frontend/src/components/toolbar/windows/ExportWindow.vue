<template>
  <ul class="flex flex-col gap-1.5 p-0 m-0 list-none">
    <li class="flex items-center justify-between gap-2 dark:text-[#c3c3c3]">
      <ExportingButton :mode="mode"></ExportingButton>
    </li>
    <li v-if="mode == 'protein'" class="flex items-center justify-between gap-2 dark:text-[#c3c3c3]">
      <ExportGraph></ExportGraph>
    </li>
    <li v-if="mode == 'protein'" class="flex items-center justify-between gap-2 dark:text-[#c3c3c3]">
      <ExportProteins :gephi_data="gephi_data"></ExportProteins>
    </li>
    <li v-if="mode == 'protein'" class="flex items-center justify-between gap-2 dark:text-[#c3c3c3]">
      <ExportEdges :gephi_data="gephi_data" :ensembl_name_index="ensembl_name_index">
      </ExportEdges>
    </li>
  </ul>
</template>

<script>
import ExportProteins from "@/components/toolbar/modules/ExportProteins.vue";
import ExportEdges from "@/components/toolbar/modules/ExportEdges.vue";
import ExportingButton from "@/components/toolbar/modules/ExportingButton.vue";
import ExportGraph from "@/components/toolbar/modules/ExportGraph.vue";

export default {
  name: "ExportWindow",
  props: ["mode", "gephi_data", "ensembl_name_index"],
  components: {
    ExportingButton,
    ExportGraph,
    ExportProteins,
    ExportEdges,
  },
  data() {
    return {};
  },
};
</script>
