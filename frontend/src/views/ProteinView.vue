<template>
  <div class="protein-view">
    <keep-alive>
      <MainVis ref="mainVis"
        :active_node='active_node' @active_node_changed = 'active_node = $event'
        :active_term='active_term' @active_term_changed = 'active_term = $event'
        :active_layer='active_layer' @active_layer_changed = 'active_layer = $event'
        :active_subset='active_subset' @active_subset_changed = 'active_subset = $event'
        :gephi_data='gephi_data'
        :active_decoloumn='active_decoloumn'
        :unconnected_nodes='unconnected_nodes'
        :active_combine='active_combine' @active_decoloumn_changed = 'active_decoloumn = $event'
        :node_color_index='node_color_index'
        :edge_color_index='edge_color_index'
      ></MainVis>
      <PaneSystem
        :active_node='active_node' @active_node_changed = 'active_node = $event'
        :active_term='active_term' @active_term_changed = 'active_term = $event'
        :active_subset='active_subset' @active_subset_changed = 'active_subset = $event'
        :active_decoloumn='active_decoloumn' @active_decoloumn_changed = 'active_decoloumn = $event'
        @active_layer_changed = 'active_layer = $event'
        @active_combine_changed = 'active_combine = $event'
        :gephi_data='gephi_data'
        :node_color_index='node_color_index'
      ></PaneSystem>
      <EnrichmentTool
        :gephi_data='gephi_data'
        @active_term_changed = 'active_term = $event'
        @active_layer_changed = 'active_layer = $event'
      ></EnrichmentTool>
      <MainToolBar
        :gephi_data='gephi_data'
        @active_subset_changed = 'active_subset = $event'
      ></MainToolBar>
      <div class="header-menu">
        <ModularityClass
        :gephi_data='gephi_data'
        :active_subset='active_subset' @active_subset_changed = 'active_subset = $event'
        > </ModularityClass>
      </div>
      <ToggleLabel
      :type='type'
      ></ToggleLabel>
    </keep-alive>
  </div>
</template>

<script>
// @ is an alias to /src
import MainVis from '@/components/visualization/MainVis.vue'
import PaneSystem from '@/components/pane/PaneSystem.vue'
import EnrichmentTool from '@/components/enrichment/EnrichmentTool.vue'
import ModularityClass from '../components/interface/ModularityClass.vue'
import ToggleLabel from '../components/interface/ToggleLabel.vue'
import MainToolBar from '../components/toolbar/MainToolBar.vue'

export default {
  name: 'ProteinView',
  components: {
    MainVis,
    PaneSystem,
    EnrichmentTool,
    ModularityClass,
    MainToolBar,
    ToggleLabel
  },
  data() {
    return {
      gephi_data: this.$store.state.gephi_json.data,
      active_node: null,
      active_term: null,
      active_layer: null,
      active_combine: null,
      active_decoloumn: null,
      node_color_index: null,
      edge_color_index: null,
      active_subset: null,
      unconnected_nodes: null,
      type: 'protein'
    }
  },
  activated() {

    const term = this.$store.state.enrichment
    const all_terms = this.$store.state.enrichment_terms
    if(term != null){
      for (var idx in all_terms) {
        var node = all_terms[idx];
        if(node.id == term){
          this.active_term = node
        }
      }
      this.$store.commit('assign_active_enrichment', null)
    }
  },
  mounted() {
    var com = this;

    com.node_color_index = {};
    for (var idx in com.gephi_data.nodes) {
      var node = com.gephi_data.nodes[idx];
      com.node_color_index[node.id] = node.color;
    }

    com.edge_color_index = {};
    for (var idy in com.gephi_data.edges) {
      var edge = com.gephi_data.edges[idy];
      com.edge_color_index[edge.id] = edge.color;
    }

    const maingraph = new Set(com.gephi_data.subgraph)
    com.unconnected_nodes = com.gephi_data.nodes.filter(item => !maingraph.has(item.id));

    this.emitter.on("decoloumn", state => {
      com.active_decoloumn = state
    });

  }
}
</script>

<style>

.header-menu {
  display: inline-flex;
  margin: 15px 0 0 0;
  width: 100%;
  justify-content: center;
}
</style>
