<template>
  <ul class="list-none p-0 m-0 flex flex-col divide-y dark:divide-[#343b4c]">
    <li class="flex items-center justify-between gap-2 py-2 dark:text-[#c3c3c3]">
      <ExportingButton :mode="mode"></ExportingButton>
    </li>
    <li v-if="mode == 'protein'" class="flex items-center justify-between gap-2 py-2 dark:text-[#c3c3c3]">
      <ExportGraph></ExportGraph>
    </li>
    <li v-if="mode == 'protein'" class="flex items-center justify-between gap-2 py-2 dark:text-[#c3c3c3]">
      <ExportProteins :gephi_data="gephi_data"></ExportProteins>
    </li>
    <li v-if="mode == 'protein'" class="flex items-center justify-between gap-2 py-2 dark:text-[#c3c3c3]">
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
