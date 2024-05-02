<template>
    <div class="visualization">
      <div id="sigma-canvas" class="sigma-parent" ref="sigmaContainer" @contextmenu.prevent="handleSigmaContextMenu">
      </div>
    </div>
  </template>

<script>
import sigma from 'sigma'
import saveAsPNG from '../../rendering/saveAsPNG';
import saveAsSVG from '../../rendering/saveAsSVG';
import customLabelRenderer from '../../rendering/customLabelRenderer';
import customNodeRenderer from '../../rendering/customNodeRenderer';
import sigmaRenderer from '../../rendering/sigma_renderer';

sigma.canvas.labels.def = customLabelRenderer
sigma.canvas.nodes.def = customNodeRenderer
sigma.renderers.canvas.prototype.resize = sigmaRenderer;

var sigma_instance = null;



export default {
  name: 'CitationVis',
  props: ['citation_data', 'active_node', 'node_color_index','node_size_index', 'edge_color_index', 'unconnected_nodes', 'active_fdr', 'active_combine', 'active_subset','active_layer', 'subactive_subset','node_modul_index'],
  emits: ['active_node_changed', 'active_fdr_changed', 'active_subset_changed', 'active_layer_changed'],
  data() {
    return {
      highlight_opacity: 0.2,
      base_opacity: 0.2,
      graph_state: null,
      special_label: false,
      sigma_instance: null,
    }
  },
  watch: {
    citation_data(){
      const com = this

      sigma_instance.graph.clear();
      sigma_instance.graph.read(com.citation_data);

      if(com.graph_state) this.show_unconnectedGraph(com.graph_state);

      com.edit_opacity('full')

      if(com.active_node) this.$emit('active_node_changed', sigma_instance.graph.getNodeFromIndex(com.active_node.id));

      sigma_instance.refresh()

    },
    active_node(node) {
      var com = this;
      
      com.reset()

      if(node == null) {
        com.resetFocus(sigma_instance.cameras[0])
        return
      }

      var sigma_node = sigma_instance.graph.getNodeFromIndex(node.attributes["Ensembl ID"])

      com.focusNode(sigma_instance.cameras[0] , sigma_node)

      const neighbors = new Set();
      const highlighted_edges = new Set();
      const edges = sigma_instance.graph.edges()
      
      sigma_node.color = "rgb(255, 255, 255)"
      if(com.special_label) {
        sigma_node.sActive = true
      }
      else sigma_node.active = true;

      for (let i = 0; i < edges.length; i++) {
        const e = edges[i]
        if (e.source === sigma_node.attributes["Ensembl ID"]) {
          neighbors.add(e.target);
          e.color = "rgb(255, 255, 255," + com.highlight_opacity + ")"
          highlighted_edges.add(e)
        } else if (e.target === sigma_node.attributes["Ensembl ID"]) {
          neighbors.add(e.source);
          highlighted_edges.add(e)
          e.color = "rgb(255, 255, 255," + com.highlight_opacity + ")"
        } else {
          e.color = "rgba(0, 100, 100," + com.base_opacity + ")"
        }
      }

      const nodes = sigma_instance.graph.nodes();
      for (let i = 0; i < nodes.length; i++) {
        const n = nodes[i]
        if (!neighbors.has(n.attributes["Ensembl ID"]) && n.attributes["Ensembl ID"] !== sigma_node.attributes["Ensembl ID"]) {
          n.color = "rgb(0, 100, 100)"
          n.active = false;
        }else{
          n.active = true;
        }
      }

      sigma_instance.refresh();

    },

    active_combine(val){
      if(val.name == "node") this.$emit('active_node_changed', val.value)
    },
  },
  methods: {
    activeNode(event, special) {
      this.special_label = special
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

      if(com.graph_state) {
        com.unconnected_nodes.forEach(function (n) {
          var node = sigma_instance.graph.getNodeFromIndex(n.id);
          node.hidden = true
        });
      }
      com.edit_opacity('full')

      sigma_instance.refresh();
    },
    reset_label_select() {
      sigma_instance.graph.nodes().forEach(function(n) {
        n.active = false
        n.sActive = false
      });

      sigma_instance.refresh()
      },

    edit_opacity(state) {
      var com = this;

      var edges = com.$store.state.highlighted_edges

      if(state == "highlight"){


        sigma_instance.graph.edges().forEach(function (e) {
          if(edges.has(e)) e.color = e.color.replace(/[\d.]+\)$/g, com.highlight_opacity+')');
      });
        
      }
      if(state == "background"){
        sigma_instance.graph.edges().forEach(function (e) {
        if(!edges.has(e)) e.color = e.color.replace(/[\d.]+\)$/g, com.base_opacity+')');
      
      });

      }
      if(state == "full"){
        sigma_instance.graph.edges().forEach(function (e) {
        e.color = e.color.replace(/[\d.]+\)$/g, com.base_opacity+')')
      });

      }

      sigma_instance.refresh();
    },

    show_unconnectedGraph(state){
      var com = this;
      
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
      }
      
      if(state){
        com.unconnected_nodes.forEach(function (n) {
          var node = graph.getNodeFromIndex(n.id);
          node.hidden = true
        });
      }   
      sigma_instance.refresh();
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
  },
  focusNode(camera, node) {
    sigma.misc.animation.camera(
      camera,
      {
        x: node['read_cam0:x'],
        y: node['read_cam0:y'],
        ratio: 0.5,
      },
      {
        duration: 1000,
      },
    );   
  },
  resetFocus(camera){

    sigma.misc.animation.camera(
      camera,
      {
        x: 0,
        y: 0,
        ratio: 1,
      },
      {
        duration: 1000,
      },
    );   
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
        labelThreshold: 10,
        minArrowSize: 10
      }
    });

    sigma_instance.graph.clear();
    sigma_instance.graph.read(com.citation_data);

    sigma_instance.graph.edges().forEach(function (edge) {
      edge["type"] = "arrow"
    });

    com.edit_opacity('full')

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




    this.emitter.on("unconnectedGraph", (state) => {
      if(state.mode=="term") this.show_unconnectedGraph(state.check)
    });
    
    this.emitter.on("searchNode", (state) => {
      if(state.mode=="term") this.$emit('active_node_changed', sigma_instance.graph.getNodeFromIndex(state.node.id))
    });
    
    
    this.emitter.on("centerGraph", (state) => {
      if(state.mode=="term") {
        sigma_instance.camera.goTo({ x: 0, y: 0, ratio: 1, angle: sigma_instance.camera.angle });
      }
    });
    
    this.emitter.on("exportGraph", (state) => {
      if(state.mode=="term") this.exportGraphAsImage(state.params)
    });

    this.emitter.on("resetSelect", (state) => {
      if(state.mode=="term") this.reset_label_select()
    });

    this.emitter.on("hideLabels", (state) => {
      if(state.mode=="term") this.hide_labels(state.check)
    });

    this.emitter.on("changeOpacity", (state) => {
      if(state.mode=="term") {
        if(state.value.layers == "highlight") com.highlight_opacity = state.value.opacity;
        else com.base_opacity = state.value.opacity;
  
        
        com.edit_opacity(state.value.layers)
      }
    });

    sigma_instance.refresh()
        
  },
  activated() {
    sigma_instance.refresh()
  }
}
</script>

<style>
</style>
  
  