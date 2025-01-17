<template>
  <div v-show="active_decoloumn !== null">
    <header v-if="active_decoloumn !== null" class="flex flex-wrap items-center gap-2">
      <span class="text-sm font-normal">{{ active_decoloumn }}</span>
    </header>

    <Tabs :value="active_section">
      <div
        :class="`${active_section ? '!pt-2 !border-t !border-slate-700 !mt-2' : ''} px-2.5 -mx-2.5 max-h-[10rem] overflow-auto overflow-x-visible`">
        <TabPanels class="!p-0">
          <TabPanel value="informations" v-show="tool_active && active_section == 'informations'">
            <h3 class="mb-1 text-sm font-medium">
              Informations
            </h3>
          </TabPanel>
          <TabPanel value="statistics" v-show="tool_active && active_section == 'statistics'">
            <h3 class="mb-1 text-sm font-medium">
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
          <Tab v-on:click="change_section('informations')" value="informations" class="!p-0 !border-0"><span
              :class="`material-symbols-rounded !text-lg ${active_section == 'informations' ? 'font-variation-ico-filled' : ''}`">info</span>
          </Tab>
          <Tab v-on:click="change_section('statistics')" value="statistics" class="!p-0 !border-0"><span
              :class="`material-symbols-rounded !text-lg ${active_section == 'statistics' ? 'font-variation-ico-filled' : ''}`">tune</span>
          </Tab>
        </TabList>
      </footer>
    </Tabs>
  </div>
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