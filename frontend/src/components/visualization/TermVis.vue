<template>
    <div id="sigma-webgl">
    </div>
  </template>

<script>
import sigma from 'sigma'
import Graph from 'graphology'

var sigma_instance = null;


export default {
  name: 'TermVis',
  props: ['term_data', 'active_node', 'node_color_index', 'edge_color_index'],
  emits: ['active_node_changed'],
  data() {
    return {
    }
  },
  watch: {
    active_node(node) {
      var com = this;

      com.reset()

      if(node == null) return

      const neighbors = new Set();
      const edges = sigma_instance.graph.edges()

      for (let i = 0; i < edges.length; i++) {
        const e = sigma_instance.graph.getEdgeAttributes(edges[i])
        if (e.source === node.attributes["Ensembl ID"]) {
          neighbors.add(e.target);
          e.color = "rgb(255, 255, 255)"
        } else if (e.target === node.attributes["Ensembl ID"]) {
          neighbors.add(e.source);
          e.color = "rgb(255, 255, 255)"
        }else{
          e.hidden = true
        }
      }

      const nodes = sigma_instance.graph.nodes();
      for (let i = 0; i < nodes.length; i++) {
        const n = sigma_instance.graph.getNodeAttributes(nodes[i])
        if (!neighbors.has(n.attributes["Ensembl ID"]) && n.attributes["Ensembl ID"] !== node.attributes["Ensembl ID"]) {
          n.hidden = true
        }
        if(n.attributes["Ensembl ID"] == node.attributes["Ensembl ID"]) n.color = "rgb(255, 255, 255)";
      }

      

      sigma_instance.refresh();

    },
    centering_active(){
      sigma_instance.camera.setState({
          x: 0.5,
          y: 0.5,
          ratio: 1,
          angle: 0
      });
    }
  },
  methods: {
    activeNode(event) {
      this.$emit('active_node_changed', event)
    },
    reset() {
      var com = this;

      sigma_instance.graph.edges().forEach(function(e) {
      const edge = sigma_instance.graph.getEdgeAttributes(e);
      const s = sigma_instance.graph.getNodeAttributes(edge.source);
      const t = sigma_instance.graph.getNodeAttributes(edge.target);
      s.color = `${com.node_color_index[edge.source]}`; s.hidden = false;
      t.color = `${com.node_color_index[edge.target]}`; t.hidden = false;
      edge.color = `${com.edge_color_index[edge.id]}`; edge.hidden = false;
    });

      sigma_instance.refresh();
    }
  },
  mounted() {
    var com = this;

    //Initializing the sigma instance to draw graph network
    const graph = new Graph();
    com.term_data.nodes.forEach(node => {
      var { id, x, y, color, size, label, attributes, hidden } = node;
      size = size*0.4
      graph.addNode(id, { x, y, color, size, label, attributes, hidden});
    });

    com.term_data.edges.forEach(edge => {
      var { id, source, target, attributes, color } = edge;
      var size = 0.2
      color = color.replace(/rgba/g, 'rgb').replace(/,[^,)]*\)/g, '').replace(/\(\d+,\d+,\d+/g, '$&)')
      graph.addEdge(source, target, { id, source, target, attributes, color, size});
    });

    const container = document.getElementById("sigma-webgl")
    const settings = {
        labelColor: {color: '#fff'},
        allowInvalidContainer: true
      }

    sigma_instance = new sigma(graph, container, settings);

    sigma_instance.on('clickNode',(event) => {
      this.activeNode(sigma_instance.graph.getNodeAttributes(event.node))
    });

    sigma_instance.refresh()
        
  }
}
</script>

<style>
  #sigma-webgl {
    position: absolute;
    width: 100%;
    height: 100%;
  }
</style>
  
  