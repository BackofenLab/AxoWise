<template>
  <div class="protein-view">
    <GraphDataProvider :backend_data="backend_data">
      <template #default="{ graph }">
        <GraphContainer v-if="graph" :graph="graph"/>
      </template>
    </GraphDataProvider>
    <VerticalPane
      :gephi_data="backend_data"
    ></VerticalPane>
  </div>
</template>

<script>
import GraphDataProvider from "@/graph/GraphDataProvider.vue";
import GraphContainer from "@/graph/GraphContainer.vue";
import VerticalPane from "@/components/verticalpane/VerticalPane.vue";

export default {
  name: "ProteinView",
  components: {
    GraphDataProvider,
    GraphContainer,
    VerticalPane
  },
  data() {
    return {
      backend_data: this.$store.state.gephi_json.data,
    };
  },
};
</script>
