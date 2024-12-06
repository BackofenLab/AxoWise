<template>
  <TabPanels class="h-[calc(100%-34px)] flex flex-col !p-0 !px-3 overflow-auto">
    <TabPanel class="flex-1" value="list">
      <PathwayList :gephi_data="gephi_data" :terms="terms" :await_load="await_load"
        :favourite_pathways="favourite_pathways" @favourite_pathways_changed="favourite_pathways = $event"
        @filtered_terms_changed="filtered_terms = $event"></PathwayList>
    </TabPanel>

    <TabPanel class="flex-1" value="graph">
      <PathwayTools :gephi_data="gephi_data" :filtered_terms="filtered_terms" :favourite_pathways="favourite_pathways"
        :mode="mode">
      </PathwayTools>
    </TabPanel>

    <TabPanel class="flex-1" value="citation">
      <CitationMenu :active_node="active_node" :active_background="active_background"></CitationMenu>
    </TabPanel>

    <TabPanel class="flex-1" value="set">
      <PathwaySet :gephi_data="gephi_data" :api="api" :mode="mode"></PathwaySet>
    </TabPanel>

    <TabPanel class="flex-1" value="layers">
      <PathwayLayers :active_termlayers="active_termlayers" :gephi_data="gephi_data" />
    </TabPanel>

    <TabPanel class="flex-1" value="heatmap">
      <HeatmapTool :mode="mode" :gephi_data="gephi_data" :filtered_terms="filtered_terms"
        :favourite_pathways="favourite_pathways">
      </HeatmapTool>
    </TabPanel>

    <TabPanel class="flex-1" value="difexp" v-if="dcoloumns">
      <DifExpMenu :active_decoloumn="active_decoloumn" :gephi_data="gephi_data" />
    </TabPanel>
  </TabPanels>
</template>

<script>
import PathwayList from "@/components/enrichment/PathwayList.vue";
import PathwayTools from "@/components/enrichment/PathwayTools.vue";
import HeatmapTool from "@/components/enrichment/HeatmapTool.vue";
import PathwaySet from "@/components/enrichment/PathwaySet.vue";
import CitationMenu from "@/components/citation/CitationMenu.vue";
import PathwayLayers from "@/components/pane/modules/layer/PathwayLayers.vue";
import DifExpMenu from "@/components/pane/modules/difexp/DifExpMenu.vue";

export default {
  name: "TabPanelOption",
  props: ["mode", "modelValue", "gephi_data", "active_decoloumn", "active_node", "active_background", "active_termlayers", "terms", "api", "await_load"],
  emits: ["update:modelValue"],
  components: {
    PathwayList,
    PathwayTools,
    PathwaySet,
    HeatmapTool,
    PathwayLayers,
    DifExpMenu,
    CitationMenu
  },
  data() {
    return {
      dcoloumns: this.$store.state.dcoloumns,
      favourite_pathways: [],
      filtered_terms: [],
    };
  },
  watch: {
    favourite_pathways: {
      handler(newList) {
        this.emitter.emit("updateFavouriteList", newList);
      },
      deep: true,
    },
  },
  methods: {
    setActiveTab(value) {
      this.$emit("update:modelValue", value);
    },
  },
  mounted() { },
};
</script>
