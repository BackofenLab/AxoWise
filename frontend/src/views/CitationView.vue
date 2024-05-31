<template>
  <keep-alive>
    <div class="citation-view">
      <CitationVis ref="CitationVis"
        :active_node='active_node' @active_node_changed='active_node = $event'
        :active_fdr='active_fdr' @active_fdr_changed='active_fdr = $event'
        :active_subset='active_subset' @active_subset_changed='active_subset = $event'
        :active_layer='active_layer' @active_layer_changed = 'active_layer = $event'
        :subactive_subset='subactive_subset'
        :citation_data='citation_data'
        :active_combine='active_combine'
        :centering_active='centering_active'
        :node_color_index='node_color_index'
        :edge_color_index='edge_color_index'
        :node_size_index='node_size_index'
        :node_modul_index='node_modul_index'
        :unconnected_nodes='unconnected_nodes'
      ></CitationVis>
      <VerticalPaneCitation
      :citation_data='citation_data'
      :node_index='node_index'
      ></VerticalPaneCitation>
      <CitationToolBar
      :data='citation_data'
      :active_subset='active_subset'
      ></CitationToolBar>
      <NetworkValues
      :data='citation_data'
      ></NetworkValues>
      <!-- <TermPaneSystem
        :gephi_data='term_data'
        :active_node='active_node' @active_node_changed = 'active_node = $event'
        :active_subset='active_subset' @active_subset_changed = 'active_subset = $event'
        @active_layer_changed = 'active_layer = $event'
        @active_combine_changed = 'active_combine = $event'
        :node_color_index='node_color_index'
        ></TermPaneSystem> -->
      <CitationPane
        :active_node='active_node' @active_node_changed='active_node = $event'
      ></CitationPane>
    </div>
  </keep-alive>
</template>

<script>
import CitationVis from '@/components/visualization/CitationVis.vue'
// import TermPaneSystem from '@/components/pane/TermPaneSystem.vue'
import CitationPane from '@/components/citation/CitationPane.vue'
import NetworkValues from '../components/interface/NetworkValues.vue'
import CitationToolBar from '../components/toolbar/CitationToolBar.vue'
import VerticalPaneCitation from '@/components/verticalpane/VerticalPaneCitation.vue'

export default {
  name: 'CitationView',
  components: {
    CitationVis,
    NetworkValues,
    CitationPane,
    CitationToolBar,
    // TermPaneSystem,
    VerticalPaneCitation
    
  },
  data() {
    return {
      citation_data: this.$store.state.citation_graph_data.graph,
      active_node: null,
      active_layer: null,
      active_fdr: null,
      active_subset: null,
      subactive_subset: null,
      active_combine: null,
      node_color_index: null,
      edge_color_index: null,
      node_size_index: null,
      node_index: null,
      centering_active: null,
      unconnected_nodes: null,
    }
  },
  watch: {
    citation_data() {
      const com = this;

      com.node_color_index = {};
      for (var idx in com.citation_data.nodes) {
        var node = com.citation_data.nodes[idx];
        com.node_color_index[node.id] = node.color;
      }
      com.node_index = {};
      for (var idi in com.citation_data.nodes) {
        var node = com.citation_data.nodes[idi];
        com.node_index[node.id] = node;
      }

      com.node_size_index = {};
      for (var idz in com.citation_data.nodes) {
      var nodeZ = com.citation_data.nodes[idz];
      com.node_size_index[nodeZ.id] = nodeZ.size;
      }

      com.edge_color_index = {};
      for (var idy in com.citation_data.edges) {
        var edge = com.citation_data.edges[idy];
        com.edge_color_index[edge.id] = edge.color;
      }

      com.node_cluster_index = {};
      for (var idg in com.citation_data.nodes) {
        var nodeG = com.citation_data.nodes[idg];
        var modularityClass = nodeG.attributes["Modularity Class"];
        if (!com.node_cluster_index[modularityClass]) com.node_cluster_index[modularityClass] = new Set();
        com.node_cluster_index[modularityClass].add(nodeG.attributes["Name"]);
      }
      this.$store.commit('assign_moduleCluster_term', com.node_cluster_index)

      com.node_modul_index = new Set()
      for (var idm in com.unconnected_nodes) {
        var node_m = com.unconnected_nodes[idm];
        com.node_modul_index.add(node_m.attributes["Modularity Class"])
      }
      this.$store.commit('assign_moduleIndex_term', com.node_modul_index)

      const maingraph = new Set(com.citation_data.subgraph)
      com.unconnected_nodes = com.citation_data.nodes.filter(item => !maingraph.has(item.id));
    }

  },
  activated() {
    this.change_graph()
  },
  mounted() {
    const com = this;

    com.node_color_index = {};
    for (var idx in com.citation_data.nodes) {
      var node = com.citation_data.nodes[idx];
      com.node_color_index[node.id] = node.color;
    }

    com.node_index = {};
    for (var idi in com.citation_data.nodes) {
      var node = com.citation_data.nodes[idi];
      com.node_index[node.id] = node;
    }

    com.node_size_index = {};
    for (var idz in com.citation_data.nodes) {
      var nodeZ = com.citation_data.nodes[idz];
      com.node_size_index[nodeZ.id] = nodeZ.size;
    }

    com.edge_color_index = {};
    for (var idy in com.citation_data.edges) {
      var edge = com.citation_data.edges[idy];
      com.edge_color_index[edge.id] = edge.color;
    }

    com.node_cluster_index = {};
    for (var idg in com.citation_data.nodes) {
      var nodeG = com.citation_data.nodes[idg];
      var modularityClass = nodeG.attributes["Modularity Class"];
      if (!com.node_cluster_index[modularityClass]) com.node_cluster_index[modularityClass] = new Set();
      com.node_cluster_index[modularityClass].add(nodeG.attributes["Name"]);
    }
    this.$store.commit('assign_moduleCluster_term', com.node_cluster_index)

    com.node_modul_index = new Set()
    for (var idm in com.unconnected_nodes) {
      var node_m = com.unconnected_nodes[idm];
      com.node_modul_index.add(node_m.attributes["Modularity Class"])
    }
    this.$store.commit('assign_moduleIndex_term', com.node_modul_index)

    const maingraph = new Set(com.citation_data.subgraph)
    com.unconnected_nodes = com.citation_data.nodes.filter(item => !maingraph.has(item.id));
    
    // this.emitter.on("graphChanged", () => {
    //   this.change_graph()
    // });

  },
  methods:{
    change_graph(){
      this.citation_data = this.$store.state.citation_graph_data.graph
    
      const term_node = this.$store.state.active_node_enrichment
      if(term_node != null){
        for (var idx in this.citation_data.nodes) {
          var node = this.citation_data.nodes[idx];
          if(node.attributes["Ensembl ID"] == term_node.id){
            this.active_node = this.citation_data.nodes[idx]
          }
        }
        this.$store.commit('assign_active_enrichment_node', null)
        }
    }
  }
}
</script>

<style>
.citation-view{
  background-color: #0A0A1A;
  display: flex;
}

</style>
