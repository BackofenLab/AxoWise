<template>
  <div class="text" v-show="active_subset !== null">
    <div class="gene_attribute" v-if="active_subset !== null">
      <div id="colorbar" :style="{ backgroundColor: '#0A0A1A' }"></div>
      <div class="gene_attr">Nodes:{{ number_prot }}</div>
      <div class="gene_attr">Edges:{{ number_asc }}</div>
      <div class="colorbar-img" v-on:click="show_layer()">
        <img src="@/assets/pane/invisible.png" v-if="!hide" />
        <img src="@/assets/pane/visible.png" v-if="hide" />
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
        v-if="tool_active && active_section == 'statistics'"
      >
        <div class="subsection-header">
          <span>parameter selection</span>
        </div>
        <div class="subsection-main colortype">
          <SubsetLinks
            :active_subset="active_subset"
            :mode="mode"
          ></SubsetLinks>
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
          <SubsetConnections :active_subset="subset"></SubsetConnections>
        </div>
      </div>
    </div>
    <div class="nodeattributes">
      <!-- <img
        class="icons"
        src="@/assets/toolbar/menu-burger.png"
        v-on:click="change_section('information')"
      /> -->
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
      <img
        class="icons"
        src="@/assets/toolbar/bote.png"
        v-on:click="call_chatbot(mode)"
      />
      <!-- <img  class="icons" src="@/assets/toolbar/logout.png" v-on:click="change_section(!tool_active,'routing')"> -->
    </div>
  </div>
</template>

<script>
import SubsetConnections from "@/components/pane/modules/subset/SubsetConnections.vue";
import SubsetLinks from "@/components/pane/modules/subset/SubsetLinks.vue";

export default {
  name: "SubsetPane",
  props: ["active_subset", "gephi_data", "mode", "tool_active"],
  emits: [
    "active_item_changed",
    "highlight_subset_changed",
    "tool_active_changed",
  ],
  components: {
    SubsetConnections,
    SubsetLinks,
  },
  data() {
    return {
      active_section: "",
      subset: null,
      hide: true,
      expand_proteins: false,
      subset_item: {
        value: null,
      },
      number_prot: "",
      number_asc: "",
      contained_edges: [],
      export_edges: [],
      subset_ids: [],
      expand_links: false,
    };
  },
  watch: {
    active_subset() {
      var com = this;

      if (com.active_subset == null) {
        return;
      }

      if (com.active_subset.type != "subset") {
        com.active_section = "";
        com.$emit("tool_active_changed", false);
      }

      com.subset = com.active_subset.selection
        ? com.active_subset.genes
        : com.active_subset;

      com.subset_item.value = com.subset;

      com.contained_edges = [];
      com.export_edges = [];
      com.subset_ids = [];

      var id_dict = {};
      for (var idX in com.subset) {
        id_dict[com.subset[idX].id] = com.subset[idX].label;
        com.subset_ids.push(com.subset[idX].id);
      }
      var subset_proteins = new Set(com.subset_ids);
      for (var idx in com.gephi_data.edges) {
        var edge = com.gephi_data.edges[idx];
        if (
          subset_proteins.has(edge.source) &&
          subset_proteins.has(edge.target)
        ) {
          if (edge.source != null && edge.target != null) {
            com.export_edges.push(edge);
            com.contained_edges.push({
              source: [edge.source, id_dict[edge.source]],
              target: [edge.target, id_dict[edge.target]],
            });
          }
        }
      }

      com.number_asc = com.export_edges.length.toString();
      com.number_prot = com.subset_ids.length.toString();

      com.$emit("active_item_changed", { Subset: com.subset_item });
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
      for (var link of com.subset) textToCopy.push(link.label);
      navigator.clipboard.writeText(textToCopy.join("\n"));
    },
    show_layer() {
      var com = this;

      var subset_check = this.hide
        ? com.subset.map((node) => node.attributes["Name"])
        : null;
      this.emitter.emit("hideSubset", {
        subset: subset_check,
        mode: this.mode,
      });
      com.hide = !com.hide;
    },
    call_chatbot(mode) {
      console.log(this.active_subset);
      this.emitter.emit("addToChatbot", {
        id: "subset" + this.active_subset.length,
        mode: mode,
        type: "subset",
        data: this.active_subset,
      });
    },
    /**
     * Calling the procedure in component MainVis to highlight a specific node
     * @param {dict} value - A dictionary of a single node
     */
    select_node(value) {
      this.emitter.emit("searchNode", { node: value, mode: this.mode });
    },

    // select_subset (nodes){
    //     this.emitter.emit("searchSubset", {subset:nodes, mode:this.mode});
    // }
  },
};
</script>

<style>
#colorbar-subset {
  position: relative;
  display: flex;
  border-radius: 5px;
  margin-top: 5%;
  width: 70%;
  color: white;
  align-items: center;
  text-align: center;
  justify-content: center;
  transform: translate(13.5%);
  font-family: "ABeeZee", sans-serif;
  font-size: 0.9vw;
}
#colorbar-subset .colorbar-text {
  background-color: rgb(0, 100, 100);
}

#subset-connections {
  height: 40%;
}

#subset {
  right: -10%;
}

.colorbar-img {
  position: absolute;
  display: flex;
  width: 0.9vw;
  justify-content: center;
  align-items: center;
  height: 100%;
  right: 3%;
}
</style>
