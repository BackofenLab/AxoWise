<template>
  <div v-show="active_termlayers !== null">
    <header v-if="active_termlayers !== null" class="flex flex-wrap items-center gap-2">
      <span class="flex items-center gap-1 text-sm font-medium">
        <strong class="font-normal dark:text-slate-300">pathways:</strong>
        {{ active_termlayers.main.size }}
      </span>
    </header>

    <Tabs :value="active_section" @update:value="change_section">
      <div
        :class="`${active_section ? '!pt-2 !border-t !border-slate-700 !mt-2' : ''} px-2.5 -mx-2.5 max-h-[10rem] overflow-auto overflow-x-visible`">
        <TabPanels class="!p-0">
          <TabPanel value="statistics">
            <div class="flex items-center justify-between mb-3">
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
            <h3 class="mb-3 text-sm font-medium">
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

  <!-- <div id="layerpane" class="text" v-show="active_termlayers !== null">
    <div class="gene_attribute" v-if="active_termlayers !== null">
      <div class="gene_attr">pathways: {{ active_termlayers.main.size }};</div>
    </div>

    <div :class="{
      'tool-section': !tool_active,
      'tool-section-active': tool_active,
    }">
      <div id="informations" class="subsection" v-show="tool_active && active_section == 'information'">
        <div class="subsection-header">
          <span>informations</span>
        </div>
        <div class="subsection-main colortype"></div>
      </div>
      <div id="network" class="subsection" v-show="tool_active && active_section == 'statistics'">
        <div class="subsection-header">
          <span>contained proteins</span>
          <img src="@/assets/pane/copy.png" v-on:click="copyclipboard()" />
        </div>
        <div class="subsection-main colortype">
          <LayerProteins :active_termlayers="active_termlayers" :gephi_data="gephi_data"></LayerProteins>
        </div>
      </div>
      <div id="connections" class="subsection" v-show="tool_active && active_section == 'connections'">
        <div class="subsection-header">
          <span>connections</span>
        </div>
        <div class="subsection-main colortype">
          <EnrichmentConnections :active_termlayers="active_termlayers"></EnrichmentConnections>
        </div>
      </div>
    </div>
    <div class="nodeattributes">
      <img class="icons" src="@/assets/toolbar/menu-burger.png" v-on:click="change_section('information')" />
      <img class="icons" src="@/assets/toolbar/settings-sliders.png" v-on:click="change_section('statistics')" />
      <img class="icons" src="@/assets/toolbar/proteinselect.png" v-on:click="change_section('connections')" />
    </div>
  </div> -->
</template>

<script>
import LayerProteins from "@/components/pane/modules/layer/LayerProteins.vue";
import EnrichmentConnections from "@/components/pane/modules/layer/EnrichmentConnections.vue";

export default {
  name: "EnrichmentLayerPane",
  props: ["active_termlayers", "gephi_data", "node_color_index", "tool_active"],
  emits: ["active_item_changed", "tool_active_changed"],
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
    change_section(val) {
      var com = this;

      if (com.tool_active && com.active_section == val) {
        com.active_section = "";
        com.$emit("tool_active_changed", false);
      } else {
        if (!com.tool_active) {
          com.active_section = val;
          com.$emit("tool_active_changed", true);
        }

        if (com.tool_active && com.active_section != val) {
          com.active_section = val;
          com.$emit("tool_active_changed", true);
        }
      }
    },
    copyclipboard() {
      this.emitter.emit("copyLayerConnections");
    },
  },
};
</script>

<!-- <style>
#layer-connections {
  height: 30%;
}

#pathway-layers {
  height: 30%;
}

#pathway-connections {
  height: 28%;
}
</style> -->
