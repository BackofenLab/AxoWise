<template>
    <keep-alive>
      <div class="citation-view">
        <CitationVis ref="citationVis"
          :citation_data='citation_data'
          :active_node='active_node' @active_node_changed='active_node = $event'
          :active_subset='active_subset' @active_subset_changed='active_subset = $event'
          :subactive_subset='subactive_subset'
          :active_combine='active_combine'
          :centering_active='centering_active'
          :node_color_index='node_color_index'
          :edge_color_index='edge_color_index'
          :node_size_index='node_size_index'
          :node_modul_index='node_modul_index'
          :unconnected_nodes='unconnected_nodes'
        ></CitationVis>
      </div>
    </keep-alive>
  </template>
  
  <script>
  import CitationVis from '@/components/visualization/CitationVis.vue'
  
  export default {
    name: 'CitationView',
    components: {
      CitationVis,
      
    },
    data() {
      return {
        citation_data: this.$store.state.gephi_json.data,
        active_node: null,
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
      citation_data() {
        const com = this;
  
        com.node_color_index = {};
        for (var idx in com.citation_data.nodes) {
          var node = com.citation_data.nodes[idx];
          com.node_color_index[node.id] = node.color;
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
  
  
        const maingraph = new Set(com.citation_data.subgraph)
        com.unconnected_nodes = com.citation_data.nodes.filter(item => !maingraph.has(item.id));
      }
  
    },
    mounted() {
      const com = this;
  
      com.node_color_index = {};
      for (var idx in com.citation_data.nodes) {
        var node = com.citation_data.nodes[idx];
        com.node_color_index[node.id] = node.color;
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
  
      const maingraph = new Set(com.citation_data.subgraph)
      com.unconnected_nodes = com.citation_data.nodes.filter(item => !maingraph.has(item.id));
    
  
    },
  }
  </script>
  
  <style>
  .citation-view{
    background-color: #0A0A1A;
    display: flex;
  }
  
  .citation-view .colortype{
    background: #0A0A1A;
  }
  </style>
  