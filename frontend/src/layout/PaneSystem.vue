<template>
  <DraggableView v-show="active_node !== null ||
    (active_subset !== null && active_subset.length !== 0) ||
    active_term !== null ||
    active_decoloumn !== null ||
    active_termlayers !== null ||
    paneHidden == false
    " :initialPosition="initial_drag_position"
    wrapperClass="!w-[18rem] border dark:border-slate-700 rounded-xl bg-[var(--card-bg)] shadow-curve-dark dark:shadow-curve-light"
    contentClass="!px-2.5 !py-0" handlerClass="flex justify-between items-center !px-3 !py-2">
    <template #handler>
      <h3 class="text-sm font-bold">
        {{ active_tab }}
      </h3>
      <div class="flex items-center gap-1 ml-auto">
        <Button class="w-5 h-5" size="small" text rounded plain @click="close_pane()">
          <span class="dark:text-white !text-xl material-symbols-rounded"> close </span>
        </Button>
      </div>
    </template>
    <template #content>
      <NodePane v-show="active_tab === 'Protein'" :mode="mode" :active_node="active_node"
        :node_color_index="node_color_index" :gephi_data="gephi_data" @active_item_changed="active_item = $event">
      </NodePane>
      <SubsetPane v-show="active_tab === 'Subset'" :mode="mode" :active_subset="active_subset" :gephi_data="gephi_data"
        @active_item_changed="active_item = $event" @highlight_subset_changed="highlight_subset = $event"
        @active_layer_changed="active_layer = $event"></SubsetPane>
      <TermPane v-show="active_tab === 'Pathway'" :mode="mode" :active_term="active_term" :gephi_data="gephi_data"
        @active_item_changed="active_item = $event" @highlight_subset_changed="highlight_subset = $event">
      </TermPane>
      <DEValuePane v-show="active_tab === 'Differential expression'" :mode="mode" :active_decoloumn="active_decoloumn"
        :gephi_data="gephi_data" @active_item_changed="active_item = $event"></DEValuePane>
      <EnrichmentLayerPane v-show="active_tab === 'Pathway layers'" :mode="mode" :active_termlayers="active_termlayers"
        :gephi_data="gephi_data" @active_item_changed="active_item = $event"></EnrichmentLayerPane>
    </template>
  </DraggableView>
</template>

<script>
import NodePane from "@/components/pane/modules/node/NodePane.vue";
import SubsetPane from "@/components/pane/modules/subset/SubsetPane.vue";
import TermPane from "@/components/pane/modules/pathways/TermPane.vue";
import DEValuePane from "@/components/pane/modules/difexp/DEValuePane.vue";
import EnrichmentLayerPane from "@/components/pane/modules/layer/EnrichmentLayerPane.vue";
import DraggableView from "@/components/DraggableView.vue";
import { useToast } from "primevue/usetoast";
export default {
  name: "PaneSystem",
  props: [
    "mode",
    "gephi_data",
    "active_subset",
    "active_term",
    "active_node",
    "active_background",
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
    "active_decoloumn_changed"
  ],
  components: {
    NodePane,
    SubsetPane,
    TermPane,
    DEValuePane,
    EnrichmentLayerPane,
    DraggableView
  },
  data() {
    return {
      active_item: null,
      active_dict: {},
      active_tab: "Protein",
      highlight_subset: null,
      paneHidden: true,
      initial_drag_position: { top: window.innerHeight - 115, left: window.innerWidth / 2 },
    };
  },
  watch: {
    active_item(val) {
      this.$emit("active_background_changed", val);
      this.active_tab = Object.keys(val)[0];
      if (val == null) {
        delete this.active_dict.val;
        return;
      }
      Object.assign(this.active_dict, val);
    },
  },
  methods: {
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
    this.toast = useToast();
    this.emitter.on("reset_protein", (state) => {
      this.selectTab("node", state);
    });
  },
};
</script>