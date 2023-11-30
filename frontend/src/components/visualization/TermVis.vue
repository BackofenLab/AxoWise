<template>
    <div class="visualization">
      <div id="sigma-canvas" class="sigma-parent" ref="sigmaContainer" 
           @contextmenu.prevent="handleSigmaContextMenu" @mouseleave="sigmaFocus = false" @mouseenter="sigmaFocus = true">
           <div v-show="moduleSelectionActive === true" v-for="(circle, index) in moduleSet" :key="index">
            <div class="modules" v-if="isMouseInside(circle.data) && !unconnectedActive(circle.modularity) && !mousedownrightCheck && !(mousedownleftCheck && mousemoveCheck) && sigmaFocus">
              <div class="inside" v-bind:style="getCircleStyle(circle.data)">
                <div class="modularity-class">{{ circle.modularity }}</div>
              </div>
            </div>
          </div>
      </div>
    </div>
  </template>

<script>
import sigma from 'sigma'
import {scaleLinear} from "d3-scale";
import saveAsPNG from '../../rendering/saveAsPNG';
import saveAsSVG from '../../rendering/saveAsSVG';
import customLabelRenderer from '../../rendering/customLabelRenderer';
import customNodeRenderer from '../../rendering/customNodeRenderer';
import sigmaRenderer from '../../rendering/sigma_renderer';
import smallestEnclosingCircle from 'smallest-enclosing-circle';

sigma.canvas.labels.def = customLabelRenderer
sigma.canvas.nodes.def = customNodeRenderer
sigma.renderers.canvas.prototype.resize = sigmaRenderer;

var sigma_instance = null;



export default {
  name: 'TermVis',
  props: ['term_data', 'active_node', 'node_color_index','node_size_index', 'edge_color_index', 'unconnected_nodes', 'active_fdr', 'active_combine', 'active_subset','active_layer', 'subactive_subset','node_modul_index'],
  emits: ['active_node_changed', 'active_fdr_changed', 'active_subset_changed', 'active_layer_changed'],
  data() {
    return {
      highlight_opacity: 0.2,
      base_opacity: 0.2,
      graph_state: null,
      special_label: false,
      moduleSet: null,
      sigma_instance: null,
      rectangular_select: {
        canvas: null,
        context: null,
        rectangle: {},
        active: false,
        surface_backup: null,
      }, 
      mouseX: 0,
      mouseY: 0,
      clusterDict: new Set(),
      mousedownrightCheck: false,
      mousedownleftCheck: false,
      mousemoveCheck: false,
      sigmaFocus: true,
      moduleSelectionActive: true,
    }
  },
  watch: {
    term_data(){
      const com = this

      sigma_instance.graph.clear();
      sigma_instance.graph.read(com.term_data);

      if(com.graph_state) this.show_unconnectedGraph(com.graph_state);

      com.edit_opacity('full')

      if(com.active_node) this.$emit('active_node_changed', sigma_instance.graph.getNodeFromIndex(com.active_node.id));

      sigma_instance.refresh()

    },
    active_node(node) {
      var com = this;
      
      com.reset()

      if(node == null) return

      var sigma_node = sigma_instance.graph.getNodeFromIndex(node.attributes["Ensembl ID"])

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
        }
      }

      this.$store.commit('assign_highlightedSet', highlighted_edges)

      sigma_instance.refresh();

    },
    active_fdr() {
      var com = this;

      if(!com.active_fdr){com.reset(); return}

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
      var proteins = null;

      if (subset == null) {
        com.reset()
        return;
      }
      
      proteins = new Set(subset.map(node => node.attributes["Ensembl ID"]));


      const highlighted_edges = new Set()

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
          highlighted_edges.add(edge)
        }
        else{
          sourceNode.color = "rgb(0,100,100)"
          sourceNode.active = false
        }

        // Target
        if(targetPresent) {
          targetNode.color = "rgb(255,255,255)"
          targetNode.active = true
          highlighted_edges.add(edge)
        }
        else{
          targetNode.color = "rgb(0,100,100)"
          targetNode.active = false
        }

        // Edge
        if (sourcePresent !== targetPresent) {
          edge.color = sourcePresent && !targetPresent ? "rgba(200, 255, 255," + com.highlight_opacity + ")" : "rgba(0, 100, 100," + com.base_opacity + ")";
        } else {
          edge.color = sourcePresent ? "rgba(255, 255, 255," + com.highlight_opacity + ")" : "rgba(0, 100, 100, " + com.base_opacity + ")";
        }
      }
      this.$store.commit('assign_highlightedSet', highlighted_edges)

      sigma_instance.refresh();
    },
    active_layer(layer) {
      var com = this;

      const graph = sigma_instance.graph;

      if(layer == null){
        graph.nodes().forEach(function (node) {
          node.hidden = false;
        });
        if(com.graph_state ) {
          com.unconnected_nodes.forEach(function (n) {
            var node = graph.getNodeFromIndex(n.id);
            node.hidden = true
          });
        }
        sigma_instance.refresh()
        return
      }

      var proteins = new Set(layer);

      graph.nodes().forEach(function (node) {
        if (proteins.has(node.attributes['Name'])) {
          node.hidden = false;
        } else {
          node.hidden = true;
        }
      });

      if(com.graph_state) {
        com.unconnected_nodes.forEach(function (n) {
          var node = graph.getNodeFromIndex(n.id);
          node.hidden = true
        });
      }
    
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
      this.$store.commit('assign_highlightedSet', new Set())
      com.edit_opacity('full')

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
  },
  // Rectangular select
  mousedown: function(e) {
  var com = this;
  com.mousedownleftCheck = true
  if (e.button == 2) {
    com.mousedownrightCheck = true
      // var selectedNodes = e.ctrlKey ? NETWORK.getSelectedNodes() : null;
      com.backup_surface();
      var rectangle = com.rectangular_select.rectangle;
      rectangle.startX = e.pageX - com.container.offsetLeft;
      rectangle.startY = e.pageY - com.container.offsetTop;
      com.rectangular_select.active = true;
      com.container.style.cursor = "crosshair";
  }
},
mousemove: function(e) {
    var com = this;
    this.mouseX = e.pageX;
    this.mouseY = e.pageY;
    if(com.mousedownleftCheck || com.mousedownrightCheck) com.mousemoveCheck = true
    if (com.rectangular_select.active) {
        var context = com.rectangular_select.context;
        var rectangle = com.rectangular_select.rectangle;
        com.restore_surface();
        rectangle.w = (e.pageX - com.container.offsetLeft) - rectangle.startX;
        rectangle.h = (e.pageY - com.container.offsetTop) - rectangle.startY ;
        var rectBounds = com.container.getBoundingClientRect();
        context.setLineDash([5]);
        context.strokeStyle = "rgb(82,182,229)";
        context.strokeRect(rectangle.startX - rectBounds.x, rectangle.startY, rectangle.w, rectangle.h);
        context.setLineDash([]);
        context.fillStyle = "rgba(82,182,229,"+ this.base_opacity +")";
        context.fillRect(rectangle.startX- rectBounds.x, rectangle.startY, rectangle.w, rectangle.h);
    }
},
mouseup: function(e) {
    var com = this;
    for (var element in this.moduleSet){
      if(this.isMouseInside(this.moduleSet[element].data)) this.getClusterElements(this.moduleSet[element])
    }
    com.mousedownleftCheck = false
    com.mousemoveCheck = false
    if (e.button == 2) {
        com.mousedownrightCheck = false
        com.restore_surface();
        com.rectangular_select.active = false;

        com.container.style.cursor = "default";
        com.select_nodes_rectangular();
    }
},
backup_surface: function() {
      var com = this;
      var canvas = com.rectangular_select.canvas;
      var context = com.rectangular_select.context;
      com.rectangular_select.surface_backup = context.getImageData(0, 0, canvas.width, canvas.height);
  },
  restore_surface: function() {
      var com = this;
      var context = com.rectangular_select.context;
      var surface = com.rectangular_select.surface_backup;
      context.putImageData(surface, 0, 0);
  },
  select_nodes_rectangular: function() {
      var com = this;
      const render_id = sigma_instance.renderers[0].conradId
      var rectangle = com.rectangular_select.rectangle;
      var rectBounds = com.container.getBoundingClientRect();

      var selected_nodes = [];
      var x_range = com.get_select_range(rectangle.startX - rectBounds.x, rectangle.w);
      var y_range = com.get_select_range(rectangle.startY - rectBounds.y, rectangle.h);

      var nodes = sigma_instance.graph.nodes();
      for (var i in nodes) {
          var node = nodes[i];
          if (node.hidden) continue;

          var node_XY = {
              x: node[`renderer${render_id}:x`],
              y: node[`renderer${render_id}:y`]
          };

          if (x_range.start <= node_XY.x && node_XY.x <= x_range.end && y_range.start <= node_XY.y && node_XY.y <= y_range.end) {
              selected_nodes.push(node);
          }
      }
      if (selected_nodes.length > 0) com.$emit("active_subset_changed", selected_nodes);
  },
  get_select_range: function(start, length) {
      return length > 0 ? {start: start, end: start + length} : {start: start + length, end: start};
  },
  get_module_circles () {
  
    var moduleSet = {}
    this.moduleSet = []
    const render_id = sigma_instance.renderers[0].conradId

    sigma_instance.graph.nodes().forEach(n =>{

      if(moduleSet[n.attributes["Modularity Class"]]) moduleSet[n.attributes["Modularity Class"]].push({x: n[`renderer${render_id}:x`],y: n[`renderer${render_id}:y`]});
      else moduleSet[n.attributes["Modularity Class"]] = [{x: n[`renderer${render_id}:x`],y: n[`renderer${render_id}:y`]}];
    });

    for (const element in moduleSet){

    
      this.moduleSet.push({ modularity: element, data: smallestEnclosingCircle(moduleSet[element])})

    }
},
getCircleStyle(circle){

  return {
      width: `${(circle.r+10) * 2}px`,
      height: `${(circle.r+10) * 2}px`,
      borderRadius: "50%", // Set border-radius to 50% to make it a circle
      position: "absolute", // Position absolute to control x and y coordinates
      left: `${circle.x - (circle.r+10)}px`,
      top: `${circle.y - (circle.r+10)}px`,
    };
},
  isMouseInside(circle) {
    const distance = Math.sqrt(
      Math.pow(circle.x - this.mouseX, 2) + Math.pow(circle.y - this.mouseY, 2)
    );
    return distance < circle.r + 10;
  },
  unconnectedActive(circle) {
    return (this.node_modul_index.has(circle) && this.graph_state)
  },
  getClusterElements(circle) {
    var com = this;

    if(this.unconnectedActive(circle.modularity) || !com.moduleSelectionActive) return

    var nodeSet = []
    if(this.active_subset) {
      nodeSet.push(...com.active_subset)
    }else {
      com.clusterDict = new Set()
    }

    sigma_instance.graph.nodes().forEach(function (node) {
      if (node.attributes["Modularity Class"] == circle.modularity){
        nodeSet.push(node)
      }
    });

    if(com.clusterDict.has(circle.modularity)) com.clusterDict.delete(circle.modularity)
    else com.clusterDict.add(circle.modularity)

    this.$emit('active_subset_changed', nodeSet.filter(item => com.clusterDict.has(item.attributes["Modularity Class"])))
    
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

    this.get_module_circles()

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

    // select all elements with the class "sigma-mouse"
    const sigmaMouse = document.querySelectorAll(".sigma-mouse");

    // select all elements with the class "sigma-parent"
    const sigmaParent = document.querySelectorAll(".sigma-parent");

    // set the values of the com object properties using the first element of each NodeList
    com.rectangular_select.canvas = sigmaMouse[0]
    com.container = sigmaParent[0],
    com.rectangular_select.canvas.oncontextmenu = function() { return false; };
    com.rectangular_select.canvas.onmousedown = com.mousedown;
    com.rectangular_select.canvas.onmousemove = com.mousemove;
    com.rectangular_select.canvas.onmouseup = com.mouseup;
    com.rectangular_select.context = com.rectangular_select.canvas.getContext("2d");

    this.emitter.on("unconnectedGraph", (state) => {
      if(state.mode=="term") this.show_unconnectedGraph(state.check)
    });
    
    this.emitter.on("searchNode", (state) => {
      if(state.mode=="term") this.$emit('active_node_changed', sigma_instance.graph.getNodeFromIndex(state.node.id))
    });
    
    this.emitter.on("searchSubset", (state) => {
      if(state.mode=="term") this.$emit('active_subset_changed', state.subset)
    });

    this.emitter.on("resizeCircle", () => {
      this.get_module_circles()
    });

    this.emitter.on("hideSubset", (state) => {
      if(state.mode=="term") this.$emit('active_layer_changed', state.subset)
    });

    this.emitter.on("activateFDR", state => {
      this.$emit('active_fdr_changed', state)
    });
    
    this.emitter.on("centerGraph", (state) => {
      if(state.mode=="term") {
        sigma_instance.camera.goTo({ x: 0, y: 0, ratio: 1, angle: sigma_instance.camera.angle });
        this.get_module_circles()
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

    this.emitter.on("deactivateModules", (state) => {
      if(state.mode=="term") com.moduleSelectionActive = !com.moduleSelectionActive
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
  #sigma-canvas {
    position: absolute;
    width: 100%;
    height: 100%;
  }
</style>
  
  