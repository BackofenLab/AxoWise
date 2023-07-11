<template>
    <div id="sigma-canvas" @contextmenu.prevent="handleSigmaContextMenu">
    </div>
  </template>

<script>
import sigma from 'sigma'
import {scaleLinear} from "d3-scale";
import saveAsPNG from '../../rendering/saveAsPNG';
import saveAsSVG from '../../rendering/saveAsSVG';
import customLabelRenderer from '../../rendering/customLabelRenderer';
import customNodeRenderer from '../../rendering/customNodeRenderer';

sigma.canvas.labels.def = customLabelRenderer
sigma.canvas.nodes.def = customNodeRenderer

var sigma_instance = null;



export default {
  name: 'TermVis',
  props: ['term_data', 'active_node', 'node_color_index','node_size_index', 'edge_color_index', 'unconnected_nodes', 'active_fdr', 'active_combine', 'active_subset', 'subactive_subset'],
  emits: ['active_node_changed', 'active_fdr_changed', 'active_subset_changed'],
  data() {
    return {
      edge_opacity: 0.2,
      graph_state: null,
      special_label: false
    }
  },
  watch: {
    term_data(){
      const com = this

      sigma_instance.graph.clear();
      sigma_instance.graph.read(com.term_data);

      if(com.graph_state) this.show_unconnectedGraph(com.graph_state);

      com.edit_opacity()

      if(com.active_node) this.$emit('active_node_changed', {node: sigma_instance.graph.getNodeFromIndex(com.active_node.node.id), graph:com.term_data});

      sigma_instance.refresh()

    },
    active_node(nodeDict) {
      var com = this;

      com.reset()
      
      if(nodeDict == null ) return;
      if(nodeDict.node == null) return;
      
      var node = nodeDict.node
      
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
          e.color = "rgba(0, 100, 100, 0.2)"
        }
      }

      const nodes = sigma_instance.graph.nodes();
      for (let i = 0; i < nodes.length; i++) {
        const n = sigma_instance.graph.getNodeFromIndex(nodes[i].id)
        if (!neighbors.has(n.attributes["Ensembl ID"]) && n.attributes["Ensembl ID"] !== node.attributes["Ensembl ID"]) {
          n.color = "rgb(0, 100, 100)"
        }
        if(n.attributes["Ensembl ID"] == node.attributes["Ensembl ID"]) {
          n.color = "rgb(255, 255, 255)";
          com.special_label ? node.sActive = true : node.active = true;
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
      if(val.name == "node") this.$emit('active_node_changed', {node: val.value, graph: this.terms})
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
          sourceNode.active = false
        }

        // Target
        if(targetPresent) {
          targetNode.color = "rgb(255,255,255)"
          targetNode.active = true
        }
        else{
          targetNode.color = "rgb(0,100,100)"
          targetNode.active = false
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
    subactive_subset(subset) {
      var com = this

      if (subset == null) {
        com.reset_size();
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
        if(sourcePresent) sourceNode.size = 25;
        // Target
        if(targetPresent) targetNode.size = 25;
      }

      sigma_instance.refresh();
    },
  },
  methods: {
    activeNode(event, special) {
      this.special_label = special
      this.$emit('active_node_changed', {node:event, graph:this.terms})
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

    if(com.graph_state) {
      com.unconnected_nodes.forEach(function (n) {
        var node = sigma_instance.graph.getNodeFromIndex(n.id);
        node.hidden = true
      });
    }

      sigma_instance.refresh();
    },
    reset_size() {
      var com = this;

      sigma_instance.graph.edges().forEach(function(e) {
      var s = sigma_instance.graph.getNodeFromIndex(e.source);
      var t = sigma_instance.graph.getNodeFromIndex(e.target);
      s.size = `${com.node_size_index[e.source]}`;
      t.size = `${com.node_size_index[e.target]}`;
    });
    
    sigma_instance.refresh();
  },
    reset_label_select() {
      sigma_instance.graph.nodes().forEach(function(n) {
        n.active = false
        n.sActive = false
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

      if(com.active_node) return
      
      com.graph_state = state

      if (state == null) {
        com.reset()
      }

      const graph = sigma_instance.graph

      if(!state){
        com.unconnected_nodes.forEach(function (n) {
          var node = graph.getNodeFromIndex(n.id);
          node.hidden = false
        });
        sigma_instance.refresh();
      }
      
      if(state){
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
    exportGraphAsImage(params) {
      if(params.format=="svg") saveAsSVG(sigma_instance, {download: true}, params.mode);
      else saveAsPNG(sigma_instance, {download: true}, params.mode);
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
  },
  reset_node_label(node) {
    node.active = false
    node.sActive = false
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

    if(com.graph_state) this.show_unconnectedGraph(com.graph_state);

    var keyState = {};

    document.addEventListener('keydown', function(event) {
      // Set the key state to true when the key is pressed
      keyState[event.keyCode] = true;
    });

    document.addEventListener('keyup', function(event) {
      // Reset the key state when the key is released
      keyState[event.keyCode] = false;
    });

    sigma_instance.bind('clickNode', function(event) {
      // Check if the desired key is being held down when clicking a node
      if (keyState[17] && keyState[16]) com.reset_node_label(event.data.node);
      else if (keyState[17] && !keyState[16]) com.activeNode(event.data.node, true);
      else com.activeNode(event.data.node, false);
      
    });

    this.emitter.on("searchTermNode", state => {
      this.$emit('active_node_changed', {node: sigma_instance.graph.getNodeFromIndex(state.id), graph:com.term_data})
    });

    this.emitter.on("unconnectedTermGraph", state => {
      this.show_unconnectedGraph(state)
    });

    this.emitter.on("fdrvalue", state => {
      this.$emit('active_fdr_changed', state)
    });

    this.emitter.on("exportTermGraph", (params) => {
      this.exportGraphAsImage(params)
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
  
  