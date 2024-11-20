<template>
  <div class="protein-view">
    <GraphDataProvider :backend_data="backend_data">
      <template #default="{ graph }">
        <GraphContainer v-if="graph" :graph="graph"/>
      </template>
    </GraphDataProvider>
  </div>
</template>

<script>
import GraphDataProvider from "@/graph/GraphDataProvider.vue";
import GraphContainer from "@/graph/GraphContainer.vue";

export default {
  name: "ProteinView",
  components: {
    GraphDataProvider,
    GraphContainer,
  },
  data() {
    return {
      backend_data: this.$store.state.gephi_json.data,
    };
  },
};
</script>
