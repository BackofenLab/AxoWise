<template>
  <keep-alive>
    <div class="protein-view">
      <TermVis ref="termVis"
        :active_node='active_node' @active_node_changed='active_node = $event'
        :active_fdr='active_fdr' @active_fdr_changed='active_fdr = $event'
        :active_subset='active_subset' @active_subset_changed='active_subset = $event'
        :active_layer='active_layer' @active_layer_changed = 'active_layer = $event'
        :subactive_subset='subactive_subset'
        :term_data='term_data'
        :active_combine='active_combine'
        :centering_active='centering_active'
        :node_color_index='node_color_index'
        :edge_color_index='edge_color_index'
        :node_size_index='node_size_index'
        :node_modul_index='node_modul_index'
        :unconnected_nodes='unconnected_nodes'
      ></TermVis>
      <PathwayGraphMenu
        :term_data='term_data'
      ></PathwayGraphMenu>
      <div class="header-menu">
        <TermToolBar
        :data='term_data'
        ></TermToolBar>
        <NetworkValues
        :data='term_data'
        ></NetworkValues>
        <SearchField
        :data='term_data'
        :active_node='active_node' @active_node_changed = 'active_node = $event'
        ></SearchField>
        <TermPaneSystem
          :gephi_data='term_data'
          :active_node='active_node' @active_node_changed = 'active_node = $event'
          :active_subset='active_subset' @active_subset_changed = 'active_subset = $event'
          @active_layer_changed = 'active_layer = $event'
          @active_combine_changed = 'active_combine = $event'
          :node_color_index='node_color_index'
          ></TermPaneSystem>
      </div>
      <!-- <GraphSelection
      :term_data='term_data' @term_data_changed = 'term_data = $event'
      >  
      </GraphSelection> -->
    </div>
  </keep-alive>
</template>

<script>
import TermVis from '@/components/visualization/TermVis.vue'
import TermPaneSystem from '@/components/pane/TermPaneSystem.vue'
import SearchField from '../components/interface/SearchField.vue'
import NetworkValues from '../components/interface/NetworkValues.vue'
import TermToolBar from '../components/toolbar/TermToolBar.vue'
import PathwayGraphMenu from '../components/pathwaytools/PathwayGraphMenu.vue'

export default {
  name: 'TermView',
  components: {
    TermVis,
    NetworkValues,
    TermToolBar,
    SearchField,
    TermPaneSystem,
    PathwayGraphMenu
    // GraphSelection
    
  },
  data() {
    return {
      term_data: this.$store.state.term_graph_data,
      active_node: null,
      active_layer: null,
      active_fdr: null,
      active_subset: null,
      subactive_subset: null,
      active_combine: null,
      node_color_index: null,
      edge_color_index: null,
      node_size_index: null,
      centering_active: null,
      unconnected_nodes: null,
    }
  },
  watch: {
    term_data() {
      const com = this;

      com.node_color_index = {};
      for (var idx in com.term_data.nodes) {
        var node = com.term_data.nodes[idx];
        com.node_color_index[node.id] = node.color;
      }

      com.node_size_index = {};
      for (var idz in com.term_data.nodes) {
      var nodeZ = com.term_data.nodes[idz];
      com.node_size_index[nodeZ.id] = nodeZ.size;
      }

      com.edge_color_index = {};
      for (var idy in com.term_data.edges) {
        var edge = com.term_data.edges[idy];
        com.edge_color_index[edge.id] = edge.color;
      }

      com.node_cluster_index = {};
      for (var idg in com.term_data.nodes) {
        var nodeG = com.term_data.nodes[idg];
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

      const maingraph = new Set(com.term_data.subgraph)
      com.unconnected_nodes = com.term_data.nodes.filter(item => !maingraph.has(item.id));
    }

  },
  activated() {
    this.change_graph()
  },
  mounted() {
    const com = this;

    com.node_color_index = {};
    for (var idx in com.term_data.nodes) {
      var node = com.term_data.nodes[idx];
      com.node_color_index[node.id] = node.color;
    }

    com.node_size_index = {};
    for (var idz in com.term_data.nodes) {
      var nodeZ = com.term_data.nodes[idz];
      com.node_size_index[nodeZ.id] = nodeZ.size;
    }

    com.edge_color_index = {};
    for (var idy in com.term_data.edges) {
      var edge = com.term_data.edges[idy];
      com.edge_color_index[edge.id] = edge.color;
    }

    com.node_cluster_index = {};
    for (var idg in com.term_data.nodes) {
      var nodeG = com.term_data.nodes[idg];
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

    const maingraph = new Set(com.term_data.subgraph)
    com.unconnected_nodes = com.term_data.nodes.filter(item => !maingraph.has(item.id));
    
    this.emitter.on("graphChanged", () => {
      this.change_graph()
    });

  },
  methods:{
    change_graph(){
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
    }
  }
}
</script>

<style>

</style>
