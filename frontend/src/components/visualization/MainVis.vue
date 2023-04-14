<template>
    <div id="sigma-webgl" class="sigma-parent" ref="sigmaContainer" @contextmenu.prevent="handleSigmaContextMenu">
    </div>
  </template>

<script>
import sigma from "sigma";
// import Graph from 'graphology'
import {scaleLinear} from "d3-scale";
import saveAsPNG from '../../rendering/saveAsPNG';

var sigma_instance = null;

sigma.classes.graph.addMethod('getNodeFromIndex', function(id) {
    return this.nodesIndex[id];
});

sigma.classes.graph.addMethod('ensemblIdToNode', function(ensembl_id) {
    var nodes = this.nodes();
    for (var idx in nodes) {
        var node = nodes[idx];
        if (node.attributes["Ensembl ID"] === ensembl_id)
            return node;
    }
    return null;
});

export default {
  name: 'MainVis',
  props: ['gephi_data', 'unconnected_nodes', 'active_node', 'active_term', 'active_subset', 'active_layer', 'active_decoloumn', 'active_combine','node_color_index', 'edge_color_index', 'export_graph'],
  emits: ['active_node_changed', 'active_term_changed', 'active_subset_changed', 'active_decoloumn_changed'],
  data() {
    return {
      isSelecting: false,
      startX: null,
      startY: null,
      endX: null,
      endY: null,
      rectWidth: 0,
      rectHeight: 0,
      state: null,
      edge_opacity: 0.2,
      rectangular_select: {
        canvas: null,
        context: null,
        rectangle: {},
        active: false,
        surface_backup: null,
      }, 
    }
  },
  watch: {
    gephi_data(){
      const com = this

      sigma_instance.clear()
      sigma_instance.read(com.gephi_data)
      com.edit_opacity()
      
      sigma_instance.refresh();

    },
    active_node(node) {
      var com = this;

      com.reset()

      if(node == null) return

      const neighbors = new Set();
      const edges = sigma_instance.graph.edges()
      
      node.color = "rgb(255, 255, 255)"

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
        const n = nodes[i]
        if (!neighbors.has(n.attributes["Ensembl ID"]) && n.attributes["Ensembl ID"] !== node.attributes["Ensembl ID"]) {
          n.hidden = true
        }
      }

      sigma_instance.refresh();


    },
    active_term(term) {
      const com = this;

      if(term == null) {
        com.reset()
        return
      }

      const proteins = new Set(term.proteins);
      const graph = sigma_instance.graph;

      graph.nodes().forEach(function (node) {
        if (proteins.has(node.id)) {
          node.color = "rgb(255, 255, 255)"
        } else {
          node.color = "rgb(0, 100, 0)"
        }
      });

      graph.edges().forEach(function (edge) {
        const source = graph.getNodeFromIndex(edge.source);
        const target = graph.getNodeFromIndex(edge.target);
        const source_present = proteins.has(source.attributes["Ensembl ID"]);
        const target_present = proteins.has(target.attributes["Ensembl ID"]);

        if (source_present && !target_present || !source_present && target_present) {
          edge.color = "rgba(220, 255, 220, 0.2)"
        } else if (source_present && target_present) {
          edge.color = "rgba(255, 255, 255, 0.2)"
        } else {
          edge.color = "rgba(0, 100, 0, 0.2)"
        }
      });

      if(com.state == "Main Graph" || com.state == null ) {
        com.unconnected_nodes.forEach(function (n) {
          var node = graph.getNodeFromIndex(n.id);
          node.hidden = true
        });
      }

      sigma_instance.refresh()

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
        sourceNode.color = sourcePresent ? "rgb(255, 255, 255)" : "rgb(0, 100, 100)";

        // Target
        targetNode.color = targetPresent ? "rgb(255, 255, 255)" : "rgb(0, 100, 100)";

        // Edge
        if (sourcePresent !== targetPresent) {
          edge.color = sourcePresent && !targetPresent ? "rgba(200, 255, 255, 0.2)" : "rgba(0, 100, 100, 0.2)";
        } else {
          edge.color = sourcePresent ? "rgba(255, 255, 255, 0.2)" : "rgba(0, 100, 100, 0.2)";
        }
      }
      this.$store.commit('assign_graph_subset', sigma_instance.graph)

      sigma_instance.refresh();
    },
    active_layer(layer) {
      var com = this;

      const graph = sigma_instance.graph;

      if(layer == null){
        graph.nodes().forEach(function (node) {
          node.hidden = false;
        });
        if(com.state == "Main Graph" || com.state == null ) {
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
        if (proteins.has(node.id)) {
          node.hidden = false;
        } else {
          node.hidden = true;
        }
      });

      if(com.state == "Main Graph" || com.state == null ) {
        com.unconnected_nodes.forEach(function (n) {
          var node = graph.getNodeFromIndex(n.id);
          node.hidden = true
        });
      }
    
    sigma_instance.refresh();

    },
    active_decoloumn(){
      var com = this

      if(com.active_decoloumn == null){
        com.reset()
        return
      }

      const graph = sigma_instance.graph

      for (const edge of graph.edges()) {
        const sourceNode = graph.getNodeFromIndex(edge.source);
        const targetNode = graph.getNodeFromIndex(edge.target);
        const source_value = sourceNode.attributes[com.active_decoloumn];
        const target_value = targetNode.attributes[com.active_decoloumn];

        sourceNode.color = com.get_normalize(source_value, -1, 1);
        targetNode.color = com.get_normalize(target_value, -1, 1);
        edge.color = com.get_normalize(source_value, -1, 1).replace(')', ', 0.2)').replace('rgb', 'rgba');

      }

      sigma_instance.refresh();

    },
    active_combine(val){
      if(val.name == "node") this.$emit('active_node_changed', val.value)
      if(val.name == "term") this.$emit('active_term_changed', val.value)
      if(val.name == "subset") this.$emit('active_subset_changed', val.value)
      if(val.name == "devalue") this.$emit('active_decoloumn_changed', val.value)
    },
  },
  methods: {
    activeNode(event) {
      this.$emit('active_node_changed', event)
    },
    reset() {
      var com = this;

      sigma_instance.graph.edges().forEach(function(e) {
      var s = sigma_instance.graph.getNodeFromIndex(e.source);
      var t = sigma_instance.graph.getNodeFromIndex(e.target);
      s.color = `${com.node_color_index[e.source]}`; s.hidden = false;
      t.color = `${com.node_color_index[e.target]}`; t.hidden = false;
      e.color = `${com.edge_color_index[e.id]}`; e.hidden = false;
    });

    if(com.state == "Main Graph" || com.state == null ) {
      com.unconnected_nodes.forEach(function (n) {
        var node = sigma_instance.graph.getNodeFromIndex(n.id);
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
  // Rectangular select
  mousedown: function(e) {
    var com = this;
    if (e.button == 2) {
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
          context.fillStyle = "rgba(82,182,229,"+ this.edge_opacity +")";
          context.fillRect(rectangle.startX- rectBounds.x, rectangle.startY, rectangle.w, rectangle.h);
      }
  },
  mouseup: function(e) {
      var com = this;
      if (e.button == 2) {
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
              x: node["renderer1:x"],
              y: node["renderer1:y"]
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
  exportGraphAsImage() {
    saveAsPNG(sigma_instance, {download: true})
    
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
  edit_opacity: function() {
    var com = this;
    sigma_instance.graph.edges().forEach(function (e) {
      e.color = e.color.replace(/[\d.]+\)$/g, com.edge_opacity + ')');
    });
    sigma_instance.refresh();
  },
},
  mounted() {
    var com = this;

    //Initializing the sigma instance to draw graph network

    sigma_instance= new sigma();
    var camera = sigma_instance.addCamera();

    sigma_instance.addRenderer({
      container: "sigma-webgl",
      type: "canvas",
      camera: camera,
      settings: {
        defaultLabelColor: "#FFF",
        hideEdgesOnMove: true,
        maxEdgeSize: 0.3,
        minEdgeSize: 0.3,
        minNodeSize: 1,
        maxNodeSize: 20,
        labelThreshold: 5
      }
    });

    sigma_instance.graph.clear();
    sigma_instance.graph.read(com.gephi_data);

    com.edit_opacity()

    sigma_instance.bind('clickNode',(event) => {
      this.activeNode(event.data.node)
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

    
    this.emitter.on("unconnectedGraph", state => {
      this.show_unconnectedGraph(state)
    });
    
    this.emitter.on("searchNode", state => {
      this.$emit('active_node_changed', sigma_instance.graph.getNodeFromIndex(state))
    });
    
    this.emitter.on("searchSubset", state => {
      this.$emit('active_subset_changed', state)
    });
    
    this.emitter.on("centerGraph", () => {
      sigma_instance.camera.goTo({ x: 0, y: 0, ratio: 1, angle: sigma_instance.camera.angle });
    });
    
    sigma_instance.refresh()
    
    this.emitter.on("exportGraph", () => {
      this.exportGraphAsImage()
    });
    
        
  }
}
</script>

<style>
  #sigma-webgl {
    position: absolute;
    width: 100%;
    height: 100%;
  }

  .sigma-label {
  color: #fff; /* set the font color to white */
  }
</style>
  
  