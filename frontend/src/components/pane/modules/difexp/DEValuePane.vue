<template>
  <div class="text" v-show="active_decoloumn !== null">
    <div class="gene_attribute" v-if="active_decoloumn !== null">
      <div class="deval">{{ active_decoloumn }}</div>
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
          <span>contained nodes</span>
        </div>
        <div class="subsection-main colortype">
          <RegulatedProteins
            :active_decoloumn="active_decoloumn"
            :gephi_data="gephi_data"
          ></RegulatedProteins>
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
    </div>
  </div>
</template>

<script>
import RegulatedProteins from "@/components/pane/modules/difexp/RegulatedProteins.vue";
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
        imageSrc: require("@/assets/pane/d-icon.png"),
      },
    };
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
    },
  },
};
</script>

<style>
.gene_attribute .deval {
  width: 100%;
  margin-left: 0.3vw;
  font-size: 0.8vw;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
}
</style>
