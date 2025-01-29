<template>
  <DraggableView v-show="(active_subset !== null && active_node == null) || paneHidden == false
    " :initialPosition="initial_drag_position"
    wrapperClass="!w-[18rem] border dark:border-slate-700 rounded-xl bg-[var(--card-bg)] shadow-curve-dark dark:shadow-curve-light"
    contentClass="!px-2.5 !py-0" handlerClass="flex justify-between items-center !px-3 !py-2">
    <template #handler>
      <h3 class="text-sm font-bold">
        {{ active_tab }}
      </h3>
      <div class="flex items-center gap-1 ml-auto">
        <Button class="w-5 h-5 ml-auto" size="small" text rounded plain @click="add_subset(active_subset)">
          <span class="dark:text-white !text-lg material-symbols-rounded"> add_circle </span>
        </Button>
        <Button class="w-5 h-5" size="small" text rounded plain @click="close_pane()">
          <span class="dark:text-white !text-xl material-symbols-rounded"> close </span>
        </Button>
      </div>
    </template>
    <template #content>
      <SubsetPane v-show="active_tab === 'Subset'" :mode="mode" :active_subset="active_subset" :gephi_data="gephi_data"
        @active_item_changed="active_item = $event" @highlight_subset_changed="highlight_subset = $event"
        @active_layer_changed="active_layer = $event"></SubsetPane>
    </template>
  </DraggableView>
</template>

<script>
import SubsetPane from "@/components/pane/modules/subset/SubsetPane.vue";
import DraggableView from "@/components/DraggableView.vue";
import { useToast } from "primevue/usetoast";
export default {
  name: "PaneSystem",
  props: [
    "mode",
    "gephi_data", "active_subset", "active_node", "node_color_index"
  ],
  emits: [
    "active_node_changed",
    "active_subset_changed",
    "active_combine_changed",
    "active_layer_changed",
  ],
  components: {
    SubsetPane,
    DraggableView
  },
  data() {
    return {
      active_item: null,
      active_dict: {},
      active_tab: "Subset",
      highlight_subset: null,
      paneHidden: true,
      initial_drag_position: { top: window.innerHeight - 115, left: window.innerWidth / 2 },
    };
  },
  watch: {
    active_item(val) {
      this.$emit("active_node_changed", null);
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

      if (this.active_node == null) {
        this.$emit("active_subset_changed", null);
        this.$emit("active_layer_changed", null);
      }
    },
    add_subset(subset) {
      if (subset.genes) {
        this.emitter.emit("addSubsetToSummary", subset.genes);
      } else {
        this.emitter.emit("addSubsetToSummary", subset);
      }
      this.toast.add({ severity: 'success', detail: 'Subset added to summary.', life: 4000 });
    },
    selectTab(name, tab) {
      if (name == "node") {
        this.active_tab = "node";
        this.$emit("active_node_changed", null);
        this.$emit("active_combine_changed", { value: tab, name: name });
      }
      if (name == "subset") {
        this.active_tab = "subset";
        this.$emit("active_subset_changed", null);
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