<template>
  <div id="layerpane" class="text" v-show="active_termlayers !== null">
    <div class="gene_attribute" v-if="active_termlayers !== null">
      <div class="gene_attr">pathways: {{ active_termlayers.main.size }};</div>
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
          <span>contained proteins</span>
          <img src="@/assets/pane/copy.png" v-on:click="copyclipboard()" />
        </div>
        <div class="subsection-main colortype">
          <LayerProteins
            :active_termlayers="active_termlayers"
            :gephi_data="gephi_data"
          ></LayerProteins>
        </div>
      </div>
      <div
        id="connections"
        class="subsection"
        v-show="tool_active && active_section == 'connections'"
      >
        <div class="subsection-header">
          <span>connections</span>
        </div>
        <div class="subsection-main colortype">
          <EnrichmentConnections
            :active_termlayers="active_termlayers"
          ></EnrichmentConnections>
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
        imageSrc: require("@/assets/pane/layer-icon.png"),
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

<style>
#layer-connections {
  height: 30%;
}

#pathway-layers {
  height: 30%;
}

#pathway-connections {
  height: 28%;
}
</style>
