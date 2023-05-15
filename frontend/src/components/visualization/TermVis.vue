<template>
    <div id="sigma-canvas">
    </div>
  </template>

<script>
import sigma from 'sigma'
import {scaleLinear} from "d3-scale";
import saveAsPNG from '../../rendering/saveAsPNG';

var sigma_instance = null;



export default {
  name: 'TermVis',
  props: ['term_data', 'active_node', 'node_color_index', 'edge_color_index', 'unconnected_nodes', 'active_fdr', 'active_combine', 'active_subset'],
  emits: ['active_node_changed', 'active_fdr_changed', 'active_subset_changed'],
  data() {
    return {
      edge_opacity: 0.2,
      state: null,
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
        const e = edges[i]
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
        const n = sigma_instance.graph.getNodeFromIndex(nodes[i].id)
        if (!neighbors.has(n.attributes["Ensembl ID"]) && n.attributes["Ensembl ID"] !== node.attributes["Ensembl ID"]) {
          n.hidden = true
        }
        if(n.attributes["Ensembl ID"] == node.attributes["Ensembl ID"]) {
          n.active = true
          n.color = "rgb(255, 255, 255)";
        }
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
    },
    active_fdr() {
      var com = this;

      

      if(com.active_fdr == null){com.reset(); return}

      sigma_instance.graph.edges().forEach(function (e) {
          // Nodes
          var source = sigma_instance.graph.getNodeFromIndex(e.source);
          var target = sigma_instance.graph.getNodeFromIndex(e.target);
          var source_value = 0
          var target_value = 0

          // Ensembl IDs
          if(source.attributes['FDR'] != 0) source_value = Math.abs(Math.floor(Math.log10(source.attributes['FDR'])))
          if(target.attributes['FDR'] != 0) target_value = Math.abs(Math.floor(Math.log10(target.attributes['FDR'])))
          
          source.color = com.get_normalize(source_value, 0, 10);
          target.color = com.get_normalize(target_value, 0, 10);
          e.color = com.get_normalize(source_value, 0, 10).replace(')', ', 0.2)').replace('rgb', 'rgba');
              
      });

      sigma_instance.refresh();
    },
    active_combine(val){
      if(val.name == "node") this.$emit('active_node_changed', val.value)
      if(val.name == "fdr") this.$emit('active_fdr_changed', val.value)
      if(val.name == "subset") this.$emit('active_subset_changed', val.value)
    },
    active_subset(subset) {
      var com = this

      if (subset == null) {
        com.reset();
        return
      }

      const proteins = new Set(subset.map(node => node.attributes["Ensembl ID"]));

      const graph = sigma_instance.graph;

      for (const edge of graph.edges()) {
        const sourceNode = graph.getNodeFromIndex(edge.source)
        const targetNode = graph.getNodeFromIndex(edge.target)
        const sourceID = sourceNode.attributes["Ensembl ID"];
        const targetID = targetNode.attributes["Ensembl ID"];
        const sourcePresent = proteins.has(sourceID);
        const targetPresent = proteins.has(targetID);

        // Source
        if(sourcePresent) {
          sourceNode.color = "rgb(255,255,255)"
          sourceNode.active = true
        }
        else{
          sourceNode.color = "rgb(0,100,100)"
        }

        // Target
        if(targetPresent) {
          targetNode.color = "rgb(255,255,255)"
          targetNode.active = true
        }
        else{
          targetNode.color = "rgb(0,100,100)"
        }

        // Edge
        if (sourcePresent !== targetPresent) {
          edge.color = sourcePresent && !targetPresent ? "rgba(200, 255, 255, 0.2)" : "rgba(0, 100, 100, 0.2)";
        } else {
          edge.color = sourcePresent ? "rgba(255, 255, 255, 0.2)" : "rgba(0, 100, 100, 0.2)";
        }
      }
      // this.$store.commit('assign_graph_subset', sigma_instance.graph)

      sigma_instance.refresh();
    },
  },
  methods: {
    activeNode(event) {
      this.$emit('active_node_changed', event)
    },
    reset() {
      var com = this;

      sigma_instance.graph.edges().forEach(function(e) {
      const edge = e;
      const s = sigma_instance.graph.getNodeFromIndex(edge.source);
      const t = sigma_instance.graph.getNodeFromIndex(edge.target);
      s.color = `${com.node_color_index[edge.source]}`; s.hidden = false;
      t.color = `${com.node_color_index[edge.target]}`; t.hidden = false;
      edge.color = `${com.edge_color_index[edge.id]}`; edge.hidden = false;
    });

    if(com.state == "Main Graph" || com.state == null ) {
      com.unconnected_nodes.forEach(function (n) {
        var node = sigma_instance.graph.getNodeFromIndex(n.id);
        node.hidden = true
      });
    }

      sigma_instance.refresh();
    },
    reset_label_select() {
      sigma_instance.graph.nodes().forEach(function(n) {
        n.active = false
      });

      sigma_instance.refresh()
      },
    edit_opacity: function() {
      var com = this;
      sigma_instance.graph.edges().forEach(function (e) {
        e.color = e.color.replace(/[\d.]+\)$/g, com.edge_opacity + ')');
      });
      sigma_instance.refresh();
    },
    show_unconnectedGraph(state){
      var com = this;

      com.state = state

      if (state == null) {
        com.reset()
      }

      const graph = sigma_instance.graph

      if(state == "Whole Graph"){
        com.unconnected_nodes.forEach(function (n) {
          var node = graph.getNodeFromIndex(n.id);
          node.hidden = false
        });
        sigma_instance.refresh();
      }
      
      if(state == "Main Graph"){
        com.unconnected_nodes.forEach(function (n) {
          var node = graph.getNodeFromIndex(n.id);
          node.hidden = true
        });
        sigma_instance.refresh();
      }   
    },
    get_normalize: function(data, nmin, nmax) {
    var rgb_value = scaleLinear()
      .domain([nmin, 0, nmax])
      .range(["blue", "white", "red"])(data);

    return rgb_value;
    },
    exportGraphAsImage() {
      saveAsPNG(sigma_instance, {download: true})
    },
    hide_labels(state) {
    if(state){
      sigma_instance.graph.nodes().forEach(function(n) {
        n.hide_label = true
      });
    }else{
      sigma_instance.graph.nodes().forEach(function(n) {
        n.hide_label = false
      });
    }
    sigma_instance.refresh()
  }
  },
  mounted() {
    var com = this;

    sigma_instance= new sigma();
    var camera = sigma_instance.addCamera();

    sigma_instance.addRenderer({
      container: "sigma-canvas",
      type: "canvas",
      camera: camera,
      settings: {
        defaultLabelColor: "#FFF",
        hideEdgesOnMove: true,
        maxEdgeSize: 0.3,
        minEdgeSize: 0.3,
        minNodeSize: 1,
        maxNodeSize: 20,
        labelThreshold: 10
      }
    });

    sigma_instance.graph.clear();
    sigma_instance.graph.read(com.term_data);

    com.edit_opacity()

    sigma_instance.bind('clickNode',(event) => {
      this.activeNode(event.data.node)
    });

    this.emitter.on("searchTermNode", state => {
      this.$emit('active_node_changed', sigma_instance.graph.getNodeFromIndex(state.id))
    });

    this.emitter.on("unconnectedTermGraph", state => {
      this.show_unconnectedGraph(state)
    });

    this.emitter.on("fdrvalue", state => {
      this.$emit('active_fdr_changed', state)
    });

    this.emitter.on("exportTermGraph", () => {
      this.exportGraphAsImage()
    });

    this.emitter.on("centerTermGraph", () => {
      sigma_instance.camera.goTo({ x: 0, y: 0, ratio: 1, angle: sigma_instance.camera.angle });
    });

    this.emitter.on("resetTermSelect", () => {
      this.reset_label_select()
    });

    this.emitter.on("searchTermSubset", state => {
      this.$emit('active_subset_changed', state)
    });

    this.emitter.on("hideTermLabels", (state) => {
      this.hide_labels(state)
    });

    sigma_instance.refresh()
        
  },
  activated() {
    sigma_instance.refresh()
  }
}
</script>

<style>
  #sigma-canvas {
    position: absolute;
    width: 100%;
    height: 100%;
  }
</style>
  
  