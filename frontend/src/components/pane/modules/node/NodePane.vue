<template>
  <div v-show="active_node !== null">
    <header v-if="active_node !== null" class="flex flex-wrap items-center gap-2">
      <span class="flex items-center gap-1 text-sm font-medium">
        <small class="flex-shrink-0 w-3 h-3 border rounded-full border-slate-400"
          :style="{ backgroundColor: colornode }"></small>
        <strong class="font-normal">{{ active_node.attributes["Name"] }}</strong>
      </span>
      <span class="flex items-center gap-1 text-sm font-medium">
        <strong class="font-normal dark:text-slate-300">Deg:</strong>
        {{ active_node.attributes["Degree"] }}
      </span>
      <span class="flex items-center gap-1 text-sm font-medium">
        <strong class="font-normal dark:text-slate-300">Pr:</strong>
        {{ Math.abs(active_node.attributes["PageRank"]).toExponential(2) }}
      </span>
    </header>

    <Tabs v-model:value="active_section">
      <div
        :class="`${active_section ? '!pt-2 !border-t !border-slate-700 !mt-2' : ''} px-2.5 -mx-2.5 max-h-[10rem] overflow-auto overflow-x-visible`">
        <TabPanels class="!p-0">
          <TabPanel value="informations">
            <h3 class="mb-1 text-sm font-medium">
              Information
            </h3>
            <ChatbotInformation :active_node="active_node"></ChatbotInformation>
          </TabPanel>
          <TabPanel value="statistics">
            <h3 class="mb-1 text-sm font-medium">
              Network statistics
            </h3>
            <NetworkStatistics :active_node="active_node" :mode="mode"></NetworkStatistics>
          </TabPanel>
          <TabPanel value="connections">
            <div class="flex items-center justify-between mb-1">
              <h3 class="text-sm font-medium">
                Connections
              </h3>
              <Button class="w-5 h-5" size="small" text plain rounded @click="copyclipboard()">
                <span class="dark:text-white material-symbols-rounded !text-lg"> content_copy </span>
              </Button>
            </div>
            <NodeConnections :active_node="active_node" :links="links"></NodeConnections>
          </TabPanel>
          <TabPanel value="routing">
            <h3 class="mb-1 text-sm font-medium">
              Routing
            </h3>
            <RoutingNode :active_node="active_node" :gephi_data="gephi_data"></RoutingNode>
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
          <Tab value="routing" class="!p-0 !border-0"><span
              :class="`material-symbols-rounded !text-lg ${active_section == 'routing' ? 'font-variation-ico-filled' : ''}`">logout</span>
          </Tab>
        </TabList>

        <div class="ml-auto">
          <Button class="w-5 h-5 !mr-1" size="small" text rounded plain @click="expand_collapse_tab()">
            <span :class="`dark:text-white material-symbols-rounded !text-lg`">{{ active_section ? 'expand_circle_up' :
              'expand_circle_down' }}</span>
          </Button>
          <Button class="w-5 h-5" size="small" text rounded plain @click="call_chatbot(mode)">
            <span class="dark:text-white material-symbols-rounded !text-lg">forum</span>
          </Button>
        </div>
      </footer>
    </Tabs>
  </div>
</template>

<script>
import NetworkStatistics from "@/components/pane/modules/node/NetworkStatistics.vue";
import NodeConnections from "@/components/pane/modules/node/NodeConnections.vue";
import ChatbotInformation from "@/components/pane/modules/node/ChatbotInformation.vue";
import RoutingNode from "@/components/pane/modules/node/RoutingNode.vue";
import { useToast } from "primevue/usetoast";

export default {
  name: "NodePane",
  props: [
    "active_node",
    "gephi_data",
    "node_color_index",
    "mode"
  ],
  emits: ["active_item_changed"],
  components: {
    NetworkStatistics,
    ChatbotInformation,
    NodeConnections,
    RoutingNode,
  },
  data() {
    return {
      active: true,
      active_section: "",
      links: null,
      colornode: null,
      expand_neighbor: false,
      expand_stats: false,
      node_item: {
        value: null,
      },
      nodes: this.gephi_data.nodes,
    };
  },
  mounted() {
    this.toast = useToast();
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
    to_proteins() {
      var com = this;
      this.$store.commit(
        "assign_active_enrichment",
        com.active_node.attributes["Ensembl ID"]
      );
      this.$router.push("protein");
    },
    select_node(value) {
      this.emitter.emit("searchNode", { node: value, mode: this.mode });
    },
    call_chatbot(mode) {
      this.emitter.emit("addToChatbot", {
        id: this.active_node.attributes["Name"],
        mode: mode,
        type: "protein",
        data: this.active_node,
      });
    },
    expand_collapse_tab() {
      if (this.active_section) {
        this.active_section = null;
      } else {
        this.active_section = 'informations'
      }
    },
    copyclipboard() {
      var com = this;

      var textToCopy = [];
      for (var link of com.links) textToCopy.push(link.label);
      navigator.clipboard.writeText(textToCopy.join("\n"));
      this.toast.add({ severity: 'success', detail: 'Message copied to clipboard.', life: 4000 });
    },
  },
};
</script>