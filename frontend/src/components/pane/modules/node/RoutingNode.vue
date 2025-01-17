<template>
  <IconField class="w-full mb-3">
    <InputText v-model="search_raw" placeholder="Enter target protein" class="w-full"
      @keyup.enter="retrieve_path(search_raw)" />
    <InputIcon class="z-10 pi pi-search" />
  </IconField>

  <div class="flex items-center gap-1.5">
    <strong class="text-sm font-normal dark:text-slate-400">Connection:</strong>
    <span class="flex items-center gap-1 capitalize" v-if="path !== null">
      <span :class="`material-symbols-rounded !text-lg ${path ? 'text-primary-500' : 'text-red-500'}`">
        {{ path ? 'check_circle' : 'cancel' }}
      </span>
      {{ path }}
    </span>
  </div>
</template>

<script>
export default {
  name: "RoutingNode",
  props: ["active_node", "gephi_data"],
  data() {
    return {
      search_raw: "",
      path: null,
      target_prot: null,
    };
  },
  mounted() {
    this.emitter.on("emptySet", (state) => {
      this.path = state;
    });
  },
  watch: {
    active_node() {
      if (!this.active_node) {
        this.search_raw = "";
        this.path = false;
      }
    },
  },
  methods: {
    retrieve_path(target) {
      if (!target) {
        this.emitter.emit("reset_protein", this.active_node);
        return;
      }

      this.target_prot = this.gephi_data.nodes.filter(function (node) {
        return node.attributes["Name"].toLowerCase() === target.toLowerCase();
      })[0];

      if (!this.target_prot) {
        this.path = false;
        return;
      }
      this.emitter.emit("searchPathway", {
        source: this.active_node.id,
        target: this.target_prot.id,
      });
    },
  },
};
</script>