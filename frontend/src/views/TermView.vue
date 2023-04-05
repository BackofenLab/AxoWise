<template>
  <keep-alive>
    <div class="term-view">
      <button id="termbutton" v-on:click="proteinswitch()">PROTEIN</button>
      <TermVis ref="termVis"
        :active_node='active_node' @active_node_changed='active_node = $event'
        :term_data='term_data'
        :centering_active='centering_active'
        :node_color_index='node_color_index'
        :edge_color_index='edge_color_index'
      ></TermVis>
      <TermPaneSystem
        :active_node='active_node' @active_node_changed = 'active_node = $event'
        :term_data='term_data'
        :node_color_index='node_color_index'
      ></TermPaneSystem>
      <TermSearch
        :active_node='active_node' @active_node_changed='active_node = $event'
        :term_data='term_data'
      ></TermSearch>
    </div>
  </keep-alive>
</template>

<script>
import TermVis from '@/components/visualization/TermVis.vue'
import TermSearch from '@/components/term_graph/TermSearch.vue'
import TermPaneSystem from '@/components/term_graph/TermPaneSystem.vue'

export default {
  name: 'TermView',
  components: {
    TermVis,
    TermSearch,
    TermPaneSystem
  },
  data() {
    return {
      term_data: this.$store.state.term_graph_data,
      active_node: null,
      node_color_index: null,
      edge_color_index: null,
      centering_active: null
    }
  },
  methods: {
    proteinswitch() {
      this.$router.push('protein')
    }
  },
  activated() {

    this.term_data = this.$store.state.term_graph_data

    
    const term_node = this.$store.state.active_node_enrichment
    if(term_node != null){
      for (var idx in this.term_data.nodes) {
        var node = this.term_data.nodes[idx];
        if(node.attributes["Ensembl ID"] == term_node.id){
          console.log(this.active_node)
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
      com.edge_color_index[edge.id] = edge.color.replace(/rgba/g, 'rgb').replace(/,[^,)]*\)/g, '').replace(/\(\d+,\d+,\d+/g, '$&)');
    }
  }
}
</script>

<style>

</style>
