<template>
  <div v-show="active_decoloumn !== null">
    <header v-if="active_decoloumn !== null" class="flex flex-wrap items-center gap-2">
      <span class="text-sm font-normal">{{ active_decoloumn }}</span>
    </header>

    <Tabs :value="active_section" @update:value="change_section">
      <div
        :class="`${active_section ? '!pt-2 !border-t !border-slate-700 !mt-2' : ''} px-2.5 -mx-2.5 max-h-[10rem] overflow-auto overflow-x-visible`">
        <TabPanels class="!p-0">
          <TabPanel value="statistics">
            <h3 class="mb-3 text-sm font-medium">
              Contained nodes
            </h3>
            <RegulatedProteins :active_decoloumn="active_decoloumn" :gephi_data="gephi_data"></RegulatedProteins>
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
        </TabList>
      </footer>
    </Tabs>
  </div>

  <!-- <div class="text" v-show="active_decoloumn !== null">
    <div class="gene_attribute" v-if="active_decoloumn !== null">
      <div class="deval">{{ active_decoloumn }}</div>
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
          <span>contained nodes</span>
        </div>
        <div class="subsection-main colortype">
          <RegulatedProteins :active_decoloumn="active_decoloumn" :gephi_data="gephi_data"></RegulatedProteins>
        </div>
      </div>
    </div>
    <div class="nodeattributes">
      <img class="icons" src="@/assets/toolbar/menu-burger.png" v-on:click="change_section('information')" />
      <img class="icons" src="@/assets/toolbar/settings-sliders.png" v-on:click="change_section('statistics')" />
    </div>
  </div> -->
</template>

<script>
import RegulatedProteins from "@/components/pane/modules/difexp/RegulatedProteins.vue";
import { useToast } from "primevue/usetoast";
export default {
  name: "DEValuePane",
  props: ["active_decoloumn", "gephi_data", "tool_active"],
  emits: ["active_item_changed", "tool_active_changed"],
  components: {
    RegulatedProteins,
  },
  data() {
    return {
      active_section: "",
      d_item: {
        value: null,
      },
    };
  },
  mounted() {
    this.toast = useToast();
  },
  watch: {
    active_decoloumn() {
      var com = this;

      if (com.active_decoloumn == null) return;

      this.d_item.value = com.active_decoloumn;

      com.$emit("active_item_changed", {
        "Differential expression": this.d_item,
      });
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
      var com = this;

      var textToCopy = [];
      for (var node of com.dvalueNodes) textToCopy.push(node.label);
      navigator.clipboard.writeText(textToCopy.join("\n"));
      this.toast.add({ severity: 'success', detail: 'Message copied to clipboard.', life: 4000 });
    },
  },
};
</script>

<!-- <style>
.gene_attribute .deval {
  width: 100%;
  margin-left: 0.3vw;
  font-size: 0.8vw;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
}
</style> -->
