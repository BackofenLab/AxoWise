<template>
  <ul class="flex flex-col gap-1.5 p-0 m-0 list-none">
    <li class="flex items-center justify-between gap-2 dark:text-[#c3c3c3]">
      <ExportGraphImage :mode="mode"></ExportGraphImage>
    </li>
    <li v-if="mode == 'protein'" class="flex items-center justify-between gap-2 dark:text-[#c3c3c3]">
      <ExportGraphData :mode="mode" :gephi_data="gephi_data" :ensembl_name_index="ensembl_name_index"></ExportGraphData>
    </li>
  </ul>
</template>

<script>
import ExportGraphImage from "@/components/toolbar/modules/ExportGraphImage.vue";
import ExportGraphData from "@/components/toolbar/modules/ExportGraphData.vue";

export default {
  name: "ExportList",
  props: ["mode", "gephi_data", "ensembl_name_index"],
  components: {
    ExportGraphImage,
    ExportGraphData,
  },
  data() {
    return {};
  },
};
</script>
