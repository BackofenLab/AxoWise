<template>
  <div class="text" v-show="active_node !== null">
    <div class="path_attribute" v-if="active_node !== null">
      <div id="colorbar" :style="{ backgroundColor: colornode }"></div>
      <div class="term">{{ active_node.attributes["Name"] }};</div>
      <div class="colorbar-img" v-on:click="to_proteins()">
        <img src="@/assets/pane/follow.png" />
      </div>
    </div>
    <div
      :class="{
        'tool-section': !tool_active,
        'tool-section-active': tool_active,
      }"
    >
      <div
        id="informations"
        class="subsection"
        v-show="tool_active && active_section == 'information'"
      >
        <div class="subsection-header">
          <span>informations</span>
        </div>
        <div class="subsection-main colortype"></div>
      </div>
      <div
        id="network"
        class="subsection"
        v-show="tool_active && active_section == 'statistics'"
      >
        <div class="subsection-header">
          <span>network statistics</span>
        </div>
        <div class="subsection-main colortype">
          <NetworkStatistics
            :active_node="active_node"
            :mode="mode"
          ></NetworkStatistics>
        </div>
      </div>
      <div
        id="connections"
        class="subsection"
        v-show="tool_active && active_section == 'connections'"
      >
        <div class="subsection-header">
          <span>connections</span>
          <img src="@/assets/pane/copy.png" v-on:click="copyclipboard()" />
        </div>
        <div class="subsection-main colortype">
          <NodeConnections
            :active_node="active_node"
            :links="links"
          ></NodeConnections>
        </div>
      </div>
    </div>
    <div class="nodeattributes">
      <img
        class="icons"
        src="@/assets/toolbar/menu-burger.png"
        v-on:click="change_section('information')"
      />
      <img
        class="icons"
        src="@/assets/toolbar/settings-sliders.png"
        v-on:click="change_section('statistics')"
      />
      <img
        class="icons"
        src="@/assets/toolbar/proteinselect.png"
        v-on:click="change_section('connections')"
      />
    </div>
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
  },
};
</script>

<style></style>
