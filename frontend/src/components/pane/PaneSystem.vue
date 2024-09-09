<template>
  <div
    v-show="
      active_node !== null ||
      active_subset !== null ||
      active_term !== null ||
      active_decoloumn !== null ||
      active_termlayers !== null ||
      paneHidden == false
    "
  >
    <div class="pane" id="pane" :class="{ active: tool_active }">
      <div class="pane_header" id="pane_header">
        <span>{{ active_tab }}</span>
        <img
          class="pane_close"
          src="@/assets/toolbar/cross.png"
          v-on:click="close_pane()"
        />
      </div>
      <div class="pane-window">
        <NodePane
          v-show="active_tab === 'Protein'"
          :mode="mode"
          :tool_active="tool_active"
          @tool_active_changed="tool_active = $event"
          :active_node="active_node"
          :node_color_index="node_color_index"
          :gephi_data="gephi_data"
          @active_item_changed="active_item = $event"
        ></NodePane>
        <SubsetPane
          v-show="active_tab === 'Subset'"
          :mode="mode"
          :tool_active="tool_active"
          @tool_active_changed="tool_active = $event"
          :active_subset="active_subset"
          :gephi_data="gephi_data"
          @active_item_changed="active_item = $event"
          @highlight_subset_changed="highlight_subset = $event"
          @active_layer_changed="active_layer = $event"
        ></SubsetPane>
        <TermPane
          v-show="active_tab === 'Pathway'"
          :mode="mode"
          :tool_active="tool_active"
          @tool_active_changed="tool_active = $event"
          :active_term="active_term"
          :gephi_data="gephi_data"
          @active_item_changed="active_item = $event"
          @highlight_subset_changed="highlight_subset = $event"
        ></TermPane>
        <DEValuePane
          v-show="active_tab === 'Differential expression'"
          :mode="mode"
          :tool_active="tool_active"
          @tool_active_changed="tool_active = $event"
          :active_decoloumn="active_decoloumn"
          :gephi_data="gephi_data"
          @active_item_changed="active_item = $event"
        ></DEValuePane>

        <EnrichmentLayerPane
          v-show="active_tab === 'Pathway layers'"
          :mode="mode"
          :tool_active="tool_active"
          @tool_active_changed="tool_active = $event"
          :active_termlayers="active_termlayers"
          :gephi_data="gephi_data"
          @active_item_changed="active_item = $event"
        ></EnrichmentLayerPane>
      </div>
    </div>
  </div>
</template>

<script>
import NodePane from "@/components/pane/modules/node/NodePane.vue";
import SubsetPane from "@/components/pane/modules/subset/SubsetPane.vue";
import TermPane from "@/components/pane/modules/pathways/TermPane.vue";
import DEValuePane from "@/components/pane/modules/difexp/DEValuePane.vue";
import EnrichmentLayerPane from "@/components/pane/modules/layer/EnrichmentLayerPane.vue";

export default {
  name: "PaneSystem",
  props: [
    "gephi_data",
    "active_subset",
    "active_term",
    "active_node",
    "active_decoloumn",
    "active_termlayers",
    "node_color_index",
  ],
  emits: [
    "active_node_changed",
    "active_term_changed",
    "active_subset_changed",
    "active_combine_changed",
    "active_layer_changed",
    "active_termlayers_changed",
    "active_background_changed",
  ],
  components: {
    NodePane,
    SubsetPane,
    TermPane,
    DEValuePane,
    EnrichmentLayerPane,
  },
  data() {
    return {
      active_item: null,
      active_dict: {},
      active_tab: "Protein",
      highlight_subset: null,
      paneHidden: true,
      mode: "protein",
      tool_active: false,
    };
  },
  watch: {
    active_item(val) {
      this.$emit("active_background_changed", val);
      if (this.active_tab != Object.keys(val)[0]) this.tool_active = false;
      this.active_tab = Object.keys(val)[0];
      if (val == null) {
        delete this.active_dict.val;
        return;
      }
      Object.assign(this.active_dict, val);
    },
  },
  methods: {
    dragElement(elmnt) {
      var pos1 = 0,
        pos2 = 0,
        pos3 = 0,
        pos4 = 0;
      if (document.getElementById(elmnt.id + "_header")) {
        // if present, the header is where you move the DIV from:
        document.getElementById(elmnt.id + "_header").onmousedown =
          dragMouseDown;
      } else {
        // otherwise, move the DIV from anywhere inside the DIV:
        elmnt.onmousedown = dragMouseDown;
      }

      function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
      }

      function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the conditions:
        var parentWidth = window.innerWidth;
        var parentHeight = window.innerHeight;
        var elementWidth = elmnt.offsetWidth;
        var elementHeight = elmnt.offsetHeight;

        // calculate the new coordinates:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;

        // Calculate the new coordinates for bottom and right
        var newBottom = parentHeight - (elmnt.offsetTop - pos2 + elementHeight);
        var newRight = parentWidth - (elmnt.offsetLeft - pos1 + elementWidth);

        // set the element's new position:
        elmnt.style.bottom = newBottom + "px";
        elmnt.style.right = newRight + "px";
      }

      function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
      }
    },
    open_pane() {
      const div = document.getElementById("attributepane");
      const paneButton = document.getElementById("panebutton");
      const paneCloseButton = document.getElementById("paneclosebutton");
      const collapseIcon = document.getElementById("collapse-icon");

      if (!div.classList.contains("pane-show")) {
        div.classList.add("pane-show");
        paneButton.style.height = "100%";
        paneCloseButton.style.visibility = "hidden";
        collapseIcon.classList.add("rotate");

        this.paneHidden = false;

        this.$emit("active_node_changed", null);
        this.$emit("active_term_changed", null);
        this.$emit("active_subset_changed", null);
        this.$emit("active_layer_changed", null);
        this.$emit("active_decoloumn_changed", null);
        this.$emit("active_termlayers_changed", null);
        this.emitter.emit("enrichTerms", null);
        this.emitter.emit("enrichSubset", null);
      } else {
        div.classList.remove("pane-show");
        paneCloseButton.style.visibility = "visible";
        paneButton.style.height = "25px";
        collapseIcon.classList.remove("rotate");
        this.paneHidden = true;
        var nameKey = Object.keys(this.active_dict)[0];
        this.selectTab(nameKey, this.active_dict[nameKey].value);
      }
    },
    close_pane() {
      this.active_dict = {};

      this.$emit("active_node_changed", null);
      this.$emit("active_term_changed", null);
      this.$emit("active_subset_changed", null);
      this.$emit("active_layer_changed", null);
      this.$emit("active_decoloumn_changed", null);
      this.$emit("active_termlayers_changed", null);
      this.$emit("active_background_changed", null);
      this.emitter.emit("reset_decoloumn");
    },
    selectTab(name, tab) {
      if (name == "node") {
        this.active_tab = "node";
        this.$emit("active_node_changed", null);
        this.$emit("active_combine_changed", { value: tab, name: name });
      }
      if (name == "term") {
        this.active_tab = "term";
        this.$emit("active_term_changed", null);
        this.$emit("active_combine_changed", { value: tab, name: name });
      }
      if (name == "subset") {
        this.active_tab = "subset";
        this.$emit("active_subset_changed", null);
        this.$emit("active_combine_changed", { value: tab, name: name });
      }
      if (name == "devalue") {
        this.active_tab = "devalue";
        this.$emit("active_decoloumn_changed", null);
        this.$emit("active_combine_changed", { value: tab, name: name });
      }
      if (name == "layers") {
        this.active_tab = "layers";
        this.$emit("active_termlayers_changed", null);
        this.$emit("active_combine_changed", { value: tab, name: name });
      }
    },
  },
  mounted() {
    this.dragElement(document.getElementById("pane"));

    this.emitter.on("reset_protein", (state) => {
      this.selectTab("node", state);
    });
  },
};
</script>

<style>
.pane {
  position: absolute;
  right: 1vw;
  bottom: 1vw;
  height: 4.5vw;
  width: 15vw;
  display: block;
  background: #d9d9d9;
  align-items: center;
  z-index: 99;
}
.active {
  height: 14.5vw;
}

.pane-window {
  position: absolute;
  height: 1.5vw;
  width: 100%;
  background: #d9d9d9;
  backdrop-filter: blur(7.5px);
  color: #0a0a1a;
  cursor: default;
}

.pane .pane_header {
  color: #0a0a1a;
  height: 1.5vw;
  width: 100%;
  padding: 0.6vw;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 0.05vw solid #0a0a1a;
}
.pane .pane_header span {
  height: 100%;
  display: flex;
  font-size: 0.9vw;
  font-family: "ABeeZee", sans-serif;
  align-items: center;
}

.pane .pane_close {
  right: 3%;
  width: 0.5vw;
  height: 0.5vw;
  position: absolute;
}
</style>
