<template>
  <div v-show="active_node !== null">
    <header v-if="active_node !== null" class="flex gap-2">
      <span class="flex gap-1 text-sm font-medium">
        <small class="flex-shrink-0 w-3 h-3 mt-1 border rounded-full border-slate-400"
          :style="{ backgroundColor: colornode }"></small>
        <strong class="font-normal line-clamp-1">{{ active_node.attributes["Name"] }}</strong>
      </span>
      <Button class="flex-shrink-0 w-5 h-5 ml-auto" size="small" text plain rounded @click="to_proteins()">
        <span class="dark:text-white material-symbols-rounded !text-lg">
          open_in_new
        </span>
      </Button>
    </header>
    <Tabs :value="active_section">
      <div
        :class="`${active_section ? '!pt-2 !border-t !border-slate-700 !mt-2' : ''} px-2.5 -mx-2.5 max-h-[10rem] overflow-auto overflow-x-visible`">
        <TabPanels class="!p-0">
          <TabPanel value="informations">
            <h3 class="mb-3 text-sm font-medium" v-show="tool_active && active_section == 'informations'">
              Informations
            </h3>

          </TabPanel>
          <TabPanel value="statistics" v-show="tool_active && active_section == 'statistics'">
            <h3 class="mb-3 text-sm font-medium">
              Network statistics
            </h3>
            <NetworkStatistics :active_node="active_node" :mode="mode"></NetworkStatistics>
          </TabPanel>
          <TabPanel value="connections" v-show="tool_active && active_section == 'connections'">
            <div class="flex items-center justify-between mb-3">
              <h3 class="text-sm font-medium">
                Connections
              </h3>
              <Button class="w-5 h-5" size="small" text plain rounded @click="copyclipboard()">
                <span class="dark:text-white material-symbols-rounded !text-lg"> content_copy </span>
              </Button>
            </div>
            <NodeConnections :active_node="active_node" :links="links"></NodeConnections>
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
          <Tab v-on:click="change_section('statistics')" value="statistics" class="!p-0 !border-0"
            v-if="active_node !== null"><span
              :class="`material-symbols-rounded !text-lg ${active_section == 'statistics' ? 'font-variation-ico-filled' : ''}`">tune</span>
          </Tab>
          <Tab v-on:click="change_section('connections')" value="connections" class="!p-0 !border-0"><span
              :class="`material-symbols-rounded !text-base ${active_section == 'connections' ? 'font-variation-ico-filled' : ''}`">hub</span>
          </Tab>
        </TabList>

        <Button class="w-5 h-5 !ml-auto" size="small" text rounded plain @click="call_chatbot(mode)">
          <span class="dark:text-white material-symbols-rounded !text-lg">forum</span>
        </Button>
      </footer>
    </Tabs>
  </div>
</template>

<script>
import NetworkStatistics from "@/components/pane/modules/node/NetworkStatistics.vue";
import NodeConnections from "@/components/pane/modules/node/NodeConnections.vue";

export default {
  name: "PathwayPane",
  props: [
    "active_node",
    "gephi_data",
    "node_color_index",
    "mode",
    "tool_active",
  ],
  emits: ["active_item_changed", "tool_active_changed"],
  components: {
    NetworkStatistics,
    NodeConnections,
  },
  data() {
    return {
      links: null,
      active_section: "",
      colornode: null,
      node_item: {
        value: null,
      },
      nodes: this.gephi_data.nodes,
    };
  },
  watch: {
    active_node() {
      var com = this;

      if (com.active_node == null) {
        return;
      }

      com.node_item.value = com.active_node;

      com.$emit("active_item_changed", { Protein: com.node_item });

      com.colornode =
        com.node_color_index[com.active_node.attributes["Ensembl ID"]];

      const neighbors = {};
      const node_id = com.active_node.attributes["Ensembl ID"];
      com.gephi_data.edges.forEach((e) => {
        if (node_id == e.source) {
          neighbors[e.target] = true;
        }
        if (node_id == e.target) {
          neighbors[e.source] = true;
        }
      });

      com.links = com.gephi_data.nodes.filter((obj) => neighbors[obj.id]);
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
      for (var link of com.links) textToCopy.push(link.label);
      navigator.clipboard.writeText(textToCopy.join("\n"));
    },
    select_node(value) {
      this.emitter.emit("searchNode", { node: value, mode: this.mode });
    },
    to_proteins() {
      var com = this;
      this.$store.commit(
        "assign_active_enrichment",
        com.active_node.attributes["Ensembl ID"]
      );
      this.$router.push("protein");
    },
    call_chatbot(mode) {
      this.emitter.emit("addToChatbot", {
        id: this.active_node.attributes["Name"],
        mode: mode,
        type: "protein",
        data: this.active_node,
      });
    },
  },
};
</script>
