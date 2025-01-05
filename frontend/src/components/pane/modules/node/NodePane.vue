<template>
  <div v-show="active_node !== null">
    <header v-if="active_node !== null" class="flex flex-wrap items-center gap-2">
      <span class="flex items-center gap-1 text-sm font-medium">
        <small class="w-3 h-3 border rounded-full border-slate-400" :style="{ backgroundColor: colornode }"></small>
        <strong class="font-normal">{{ active_node.attributes["Name"] }}</strong>
      </span>
      <span class="flex items-center gap-1 text-sm font-medium">
        <strong class="font-normal dark:text-slate-300">deg:</strong>
        {{ active_node.attributes["Degree"] }}
      </span>
      <span class="flex items-center gap-1 text-sm font-medium">
        <strong class="font-normal dark:text-slate-300">pr:</strong>
        {{ Math.abs(active_node.attributes["PageRank"]).toExponential(2) }}
      </span>
    </header>

    <Tabs :value="active_section" @update:value="change_section">
      <div
        :class="`${active_section ? '!pt-2 !border-t !border-slate-700 !mt-2' : ''} px-2.5 -mx-2.5 max-h-[10rem] overflow-auto overflow-x-visible`">
        <TabPanels class="!p-0">
          <TabPanel value="informations">
            <h3 class="mb-3 text-sm font-medium">
              Information
            </h3>
            <ChatbotInformation :active_node="active_node"></ChatbotInformation>
          </TabPanel>
          <TabPanel value="statistics">
            <h3 class="mb-3 text-sm font-medium">
              Network statistics
            </h3>
            <NetworkStatistics :active_node="active_node" :mode="mode"></NetworkStatistics>
          </TabPanel>
          <TabPanel value="connections">
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

        <Button class="w-5 h-5 !ml-auto" size="small" text rounded plain @click="call_chatbot()">
          <span class="dark:text-white material-symbols-rounded !text-lg">forum</span>
        </Button>
      </footer>
    </Tabs>
  </div>

  <!-- <div class="text" v-show="active_node !== null">
    <div class="gene_attribute" v-if="active_node !== null">
      <div id="colorbar" :style="{ backgroundColor: colornode }"></div>
      <div class="gene">{{ active_node.attributes["Name"] }};</div>
      <div class="gene_attr">deg:{{ active_node.attributes["Degree"] }};</div>
      <div class="gene_attr">
        pr:{{ Math.abs(active_node.attributes["PageRank"]).toExponential(2) }}
      </div>
    </div>
    <div :class="{
      'tool-section': !tool_active,
      'tool-section-active': tool_active,
    }">
      <div id="informations" class="subsection" v-show="tool_active && active_section == 'information'">
        <div class="subsection-header">
          <span>informations</span>
        </div>
        <div class="subsection-main colortype">
          <ChatbotInformation :active_node="active_node"></ChatbotInformation>
        </div>
      </div>
      <div id="network" class="subsection" v-show="tool_active && active_section == 'statistics'">
        <div class="subsection-header">
          <span>network statistics</span>
        </div>
        <div class="subsection-main colortype">
          <NetworkStatistics :active_node="active_node" :mode="mode"></NetworkStatistics>
        </div>
      </div>
      <div id="connections" class="subsection" v-show="tool_active && active_section == 'connections'">
        <div class="subsection-header">
          <span>connections</span>
          <img src="@/assets/pane/copy.png" v-on:click="copyclipboard()" />
        </div>
        <div class="subsection-main colortype">
          <NodeConnections :active_node="active_node" :links="links"></NodeConnections>
        </div>
      </div>
      <div id="routing" class="subsection" v-show="tool_active && active_section == 'routing'">
        <div class="subsection-header">
          <span>routing</span>
        </div>
        <div class="subsection-main colortype">
          <RoutingNode :active_node="active_node" :gephi_data="gephi_data"></RoutingNode>
        </div>
      </div>
    </div>
    <div class="nodeattributes">
      <img class="icons" src="@/assets/toolbar/menu-burger.png" v-on:click="change_section('information')" />
      <img class="icons" src="@/assets/toolbar/settings-sliders.png" v-on:click="change_section('statistics')" />
      <img class="icons" src="@/assets/toolbar/proteinselect.png" v-on:click="change_section('connections')" />
      <img class="icons" src="@/assets/toolbar/logout.png" v-on:click="change_section('routing')" />
      <img class="icons" src="@/assets/toolbar/bote.png" v-on:click="call_chatbot(mode)" />
    </div>
  </div> -->
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
    "mode",
    "tool_active",
  ],
  emits: ["active_item_changed", "tool_active_changed"],
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
    select_node(value) {
      this.emitter.emit("searchNode", { node: value, mode: this.mode });
    },
    call_chatbot() {
      this.emitter.emit("addToChatbot", {
        id: this.active_node.attributes["Name"],
        mode: this.mode,
        type: "protein",
        data: this.active_node,
      });
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

<!-- <style>
.text {
  height: 100%;
}

.gene_attribute {
  display: flex;
  font-family: "ABeeZee", sans-serif;
  align-items: center;
  color: #0a0a1a;
  padding: 0 0.5vw 0 0.5vw;
}

.tool-section {
  height: 0vw;
}

.tool-section-active {
  height: 10vw;
}

#colorbar {
  position: relative;
  display: flex;
  border-radius: 100%;
  width: 0.5vw;
  height: 0.5vw;
}

.gene {
  margin-left: 0.3vw;
  font-size: 0.9vw;
}

.gene_attr {
  font-size: 0.8vw;
  margin-left: 0.3vw;
}

.nodeattributes {
  position: absolute;
  display: flex;
  width: 100%;
  height: 2vw;
  align-items: center;
  justify-content: center;
}

.nodeattributes .icons {
  width: 0.8vw;
  height: 0.8vw;
  margin: 0 0.5vw 0 0.5vw;
}

.nodeattributes .subsection {
  margin-bottom: 4%;
  position: relative;
  width: 90%;
}

.subsection .subsection-header {
  position: absolute;
  width: 100%;
  display: flex;
  justify-content: left;
  align-items: center;
  font-family: "ABeeZee", sans-serif;
  font-size: 0.7vw;
  padding: 0.2vw 0 0 0.5vw;
  color: rgba(255, 255, 255, 0.5);
  z-index: 999;
  background-color: #0a0a1a;
}

.subsection .subsection-header img {
  position: absolute;
  width: 50%;
  right: -15%;
  display: -webkit-flex;
  padding: 1%;
  padding: 5% 23% 5% 23%;
  filter: invert(100%);
}

.subsection .subsection-main {
  height: 100%;
  width: 100%;
}

#informations,
#routing,
#network,
#connections,
#context {
  height: 100%;
}
</style> -->
