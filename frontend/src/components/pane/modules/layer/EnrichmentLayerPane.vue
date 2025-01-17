<template>
  <div v-show="active_termlayers !== null">
    <header v-if="active_termlayers !== null" class="flex flex-wrap items-center gap-2">
      <span class="flex items-center gap-1 text-sm font-medium">
        <strong class="font-normal dark:text-slate-300">Pathways:</strong>
        {{ active_termlayers.main.size }}
      </span>
    </header>

    <Tabs v-model:value="active_section">
      <div
        :class="`${active_section ? '!pt-2 !border-t !border-slate-700 !mt-2' : ''} px-2.5 -mx-2.5 max-h-[10rem] overflow-auto overflow-x-visible`">
        <TabPanels class="!p-0">
          <TabPanel value="informations">
            <h3 class="mb-1 text-sm font-medium">
              Informations
            </h3>
          </TabPanel>
          <TabPanel value="statistics">
            <div class="flex items-center justify-between mb-1">
              <h3 class="text-sm font-medium">
                Contained proteins
              </h3>
              <Button class="w-5 h-5" size="small" text plain rounded @click="copyclipboard()">
                <span class="dark:text-white material-symbols-rounded !text-lg"> content_copy </span>
              </Button>
            </div>
            <LayerProteins :active_termlayers="active_termlayers" :gephi_data="gephi_data"></LayerProteins>
          </TabPanel>
          <TabPanel value="connections">
            <h3 class="mb-1 text-sm font-medium">
              Connections
            </h3>
            <EnrichmentConnections :active_termlayers="active_termlayers"></EnrichmentConnections>
          </TabPanel>
        </TabPanels>
      </div>

      <footer class="flex items-end !mt-2 !border-t !border-slate-600 py-2">
        <TabList class="" :pt="{
          tabList: { class: '!border-0 !gap-4' },
          activeBar: { class: '!hidden' }
        }">
          <Tab value="informations" class="!p-0 !border-0"><span
              :class="`material-symbols-rounded !text-lg ${active_section == 'informations' ? 'font-variation-ico-filled' : ''}`">info</span>
          </Tab>
          <Tab value="statistics" class="!p-0 !border-0"><span
              :class="`material-symbols-rounded !text-lg ${active_section == 'statistics' ? 'font-variation-ico-filled' : ''}`">tune</span>
          </Tab>
          <Tab value="connections" class="!p-0 !border-0"><span
              :class="`material-symbols-rounded !text-base ${active_section == 'connections' ? 'font-variation-ico-filled' : ''}`">hub</span>
          </Tab>
        </TabList>
      </footer>
    </Tabs>
  </div>
</template>

<script>
import LayerProteins from "@/components/pane/modules/layer/LayerProteins.vue";
import EnrichmentConnections from "@/components/pane/modules/layer/EnrichmentConnections.vue";

export default {
  name: "EnrichmentLayerPane",
  props: ["active_termlayers", "gephi_data", "node_color_index"],
  emits: ["active_item_changed"],
  components: {
    LayerProteins,
    EnrichmentConnections,
  },
  data() {
    return {
      active_section: "",
      layer_item: {
        value: null,
      },
      terms: null,
      colorpalette: {},
      colors: "rgba(0,0,0,1)",
      term: null,
    };
  },
  watch: {
    active_termlayers: {
      handler(newList) {
        var com = this;

        console.log(com.active_termlayers);
        if (newList == null) {
          return;
        }

        com.layer_item.value = newList;

        com.$emit("active_item_changed", { "Pathway layers": com.layer_item });
      },
      deep: true,
    },
  },
  methods: {
    copyclipboard() {
      this.emitter.emit("copyLayerConnections");
    },
  },
};
</script>
