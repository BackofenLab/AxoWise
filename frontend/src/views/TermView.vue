<template>
  <keep-alive>
    <div class="term-view">
      <TermVis ref="termVis"
        :active_node='active_node' @active_node_changed='active_node = $event'
        :active_fdr='active_fdr' @active_fdr_changed='active_fdr = $event'
        :term_data='term_data'
        :active_combine='active_combine'
        :centering_active='centering_active'
        :node_color_index='node_color_index'
        :edge_color_index='edge_color_index'
        :unconnected_nodes='unconnected_nodes'
      ></TermVis>
      <TermPaneSystem
        :active_node='active_node' @active_node_changed = 'active_node = $event'
        :active_fdr='active_fdr' @active_fdr_changed='active_fdr = $event'
        :term_data='term_data'
        :node_color_index='node_color_index'
        @active_combine_changed = 'active_combine = $event'
      ></TermPaneSystem>
      <TermToolBar
      :term_data='term_data'
      ></TermToolBar>
    </div>
  </keep-alive>
</template>

<script>
import TermVis from '@/components/visualization/TermVis.vue'
import TermPaneSystem from '@/components/term_graph/TermPaneSystem.vue'
import TermToolBar from '@/components/term_graph/TermToolBar.vue'

export default {
  name: 'TermView',
  components: {
    TermVis,
    TermPaneSystem,
    TermToolBar
  },
  data() {
    return {
      term_data: this.$store.state.term_graph_data,
      active_node: null,
      active_fdr: null,
      active_combine: null,
      node_color_index: null,
      edge_color_index: null,
      centering_active: null,
      unconnected_nodes: null
    }
  },
  activated() {

    this.term_data = this.$store.state.term_graph_data

    
    const term_node = this.$store.state.active_node_enrichment
    if(term_node != null){
      for (var idx in this.term_data.nodes) {
        var node = this.term_data.nodes[idx];
        if(node.attributes["Ensembl ID"] == term_node.id){
          this.active_node = this.term_data.nodes[idx]
        }
      }
      this.$store.commit('assign_active_enrichment_node', null)
      }
  },
  mounted() {
    const com = this;

    com.node_color_index = {};
    for (var idx in com.term_data.nodes) {
      var node = com.term_data.nodes[idx];
      com.node_color_index[node.id] = node.color;
    }

    com.edge_color_index = {};
    for (var idy in com.term_data.edges) {
      var edge = com.term_data.edges[idy];
      com.edge_color_index[edge.id] = edge.color;
    }

    const maingraph = new Set(com.term_data.subgraph)
    com.unconnected_nodes = com.term_data.nodes.filter(item => !maingraph.has(item.id));
  }
}
</script>

<style>

</style>
