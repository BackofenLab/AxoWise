<template>
  <ul class="list-none p-0 m-0 flex flex-col divide-y dark:divide-[#343b4c]">
    <ConnectedGraph :mode="mode"></ConnectedGraph>
    <ShowModules :mode="mode"></ShowModules>
    <ModuleSelection :mode="mode"></ModuleSelection>
    <EdgeOpacity :mode="mode"></EdgeOpacity>
    <NodeLabelSelect :mode="mode"></NodeLabelSelect>
    <FDRValue v-if="mode == 'term'"></FDRValue>
  </ul>
</template>

<script>
import FDRValue from "@/components/toolbar/modules/FDRValue.vue";
import NodeLabelSelect from "@/components/toolbar/modules/NodeLabelSelect.vue";
import ConnectedGraph from "@/components/toolbar/modules/ConnectedGraph.vue";
import ShowModules from "@/components/toolbar/modules/ShowModules.vue";
import EdgeOpacity from "@/components/toolbar/modules/EdgeOpacity.vue";
import ModuleSelection from "@/components/toolbar/modules/ModuleSelection.vue";

export default {
  name: "SettingList",
  props: ["tools_active", "mode", "gephi_data", "ensembl_name_index"],
  components: {
    EdgeOpacity,
    NodeLabelSelect,
    ConnectedGraph,
    ModuleSelection,
    FDRValue,
    ShowModules,
  },
  data() {
    return {};
  },
};
</script>