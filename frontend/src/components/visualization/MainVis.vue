<template>
  <div class="visualization">
    <div id="sigma-webgl"></div>
    <div id="sigma-canvas" :class="{'loading': threeview}" class="sigma-parent" ref="sigmaContainer" @contextmenu.prevent="handleSigmaContextMenu">
        <img class="twoview" v-show="threeview" v-on:click="two_view" src="@/assets/share-2.png" alt="Center Icon">
    </div>
  </div>
</template>

<script>
import sigma from "sigma";
// import Graph from 'graphology'
import {scaleLinear} from "d3-scale";
import saveAsPNG from '../../rendering/saveAsPNG';
import saveAsSVG from '../../rendering/saveAsSVG';
import customLabelRenderer from '../../rendering/customLabelRenderer';
import customNodeRenderer from '../../rendering/customNodeRenderer';
import ForceGraph3D from '3d-force-graph';
import "@/rendering/astarAlgorithm.js"
import randomColorRGB from 'random-color-rgb'

sigma.canvas.labels.def = customLabelRenderer
sigma.canvas.nodes.def = customNodeRenderer

var sigma_instance = null;
var three_instance = null;

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
  props: ['gephi_data', 'unconnected_nodes', 'active_node', 'active_term', 'active_subset','active_termlayers','subactive_subset', 'active_layer', 'active_decoloumn', 'active_combine','node_color_index','node_size_index', 'edge_color_index', 'export_graph'],
  emits: ['active_node_changed', 'active_term_changed', 'active_subset_changed', 'active_decoloumn_changed', 'active_termlayers_changed', 'subactive_subset_changed'],
  data() {
    return {
      threeview: false,
      isSelecting: false,
      startX: null,
      startY: null,
      endX: null,
      endY: null,
      rectWidth: 0,
      rectHeight: 0,
      state: null,
      edge_opacity: 0.3,
      rectangular_select: {
        canvas: null,
        context: null,
        rectangle: {},
        active: false,
        surface_backup: null,
      }, 
      label_active_dict: {},
      special_label: false,
      colorPalette: {}
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

      if(com.three_view) var sigma_node = sigma_instance.graph.getNodeFromIndex(node.id);
      else sigma_node = node

      const neighbors = new Set();
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
          e.color = "rgb(255, 255, 255)"
        } else if (e.target === sigma_node.attributes["Ensembl ID"]) {
          neighbors.add(e.source);
          e.color = "rgb(255, 255, 255)"
        } else {
          e.color = "rgba(0, 100, 100, 0.2)"
        }
      }

      const nodes = sigma_instance.graph.nodes();
      for (let i = 0; i < nodes.length; i++) {
        const n = nodes[i]
        if (!neighbors.has(n.attributes["Ensembl ID"]) && n.attributes["Ensembl ID"] !== sigma_node.attributes["Ensembl ID"]) {
          n.color = "rgb(0, 100, 100)"
        }
      }

      sigma_instance.refresh();

      if(com.threeview){
        if(node.active){    
          const nodesById = Object.fromEntries(three_instance.graphData().nodes.map(node3d => [node3d.id, node3d]));
          node = nodesById[node.id]
        }

        const distance = 40;
        const distRatio = 1 + distance/Math.hypot(node.x, node.y, node.z);

        const newPos = node.x || node.y || node.z
          ? { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }
          : { x: 0, y: 0, z: distance }; // special case if node is in (0,0,0)

        three_instance.cameraPosition(
          newPos, // new position
          node, // lookAt ({ x, y, z })
          3000  // ms transition duration
        );
      }


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
          node.active = true
        } else {
          node.color = "rgb(0, 100, 0)"
          node.active = false
        }
      });

      graph.edges().forEach(function (edge) {
        const source = graph.getNodeFromIndex(edge.source);
        const target = graph.getNodeFromIndex(edge.target);
        const source_present = proteins.has(source.attributes["Ensembl ID"]);
        const target_present = proteins.has(target.attributes["Ensembl ID"]);

        if (source_present && !target_present || !source_present && target_present) {
          edge.color = "rgba(220, 255, 220, 0.25)"
        } else if (source_present && target_present) {
          edge.color = "rgba(255, 255, 255, 0.3)"
        } else {
          edge.color = "rgba(0, 100, 0, 0.2)"
        }
      });

      if(com.graph_state) {
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
      this.$store.commit('assign_graph_subset', sigma_instance.graph)

      sigma_instance.refresh();
    },
    subactive_subset(subset) {
      var com = this

      if (subset == null) {
        com.reset_size();
        return
      }

      var proteins;

      if(subset[0].attributes) {
        proteins = new Set(subset.map(node => node.attributes["Ensembl ID"]));
        }
      else { 
        proteins = new Set(subset) 
      }

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
        if (proteins.has(node.id)) {
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
    active_termlayers: {
      handler(newList) {

        if (newList == null) {
          this.reset();
          return;
        }

        var visibleTermlayers = [...newList.main]
        var hiddenTermLayer = newList.hide
        
        const filteredArray = new Set(visibleTermlayers.filter(value => !hiddenTermLayer.has(value)));
        
        var proteinList = new Set()

        for (const terms of filteredArray) {
          var proteinSet = new Set([...terms.proteins]);
          proteinList = new Set([...proteinList, ...proteinSet]);
          if (!this.colorPalette[terms.name])
            this.colorPalette[terms.name] = randomColorRGB();
        }

        this.$store.commit('assign_colorpalette', this.colorPalette)

        sigma_instance.graph.nodes().forEach((n) => {
          let count = 0;
          n.color = "rgb(0,100,100)";
          for (const terms of filteredArray) {
            if (terms.proteins.includes(n.attributes["Ensembl ID"])) {
              count++;
              n.color = this.colorPalette[terms.name];
              if (count === filteredArray.size) {
                n.color = "rgb(255,255,255)";
                break;
              }
            }
          }
        });

        sigma_instance.graph.edges().forEach((e) => {
          var source = sigma_instance.graph.getNodeFromIndex(e.source);
          if(proteinList.has(e.source) && proteinList.has(e.target) ) e.color = source.color.replace(")", ", 0.5)").replace("rgb", "rgba");
          else e.color = "rgba(0,100,100,0.2)";
        });

        sigma_instance.refresh();
      },
      deep: true,
    },
    
    active_combine(val){
      if(val.name == "node") this.$emit('active_node_changed', val.value)
      if(val.name == "term") this.$emit('active_term_changed', val.value)
      if(val.name == "subset") this.$emit('active_subset_changed', val.value)
      if(val.name == "devalue") this.$emit('active_decoloumn_changed', val.value)
      if(val.name == "layers") this.$emit('active_termlayers_changed', val.value)
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
      var s = sigma_instance.graph.getNodeFromIndex(e.source);
      var t = sigma_instance.graph.getNodeFromIndex(e.target);
      s.color = `${com.node_color_index[e.source]}`; s.hidden = false;
      t.color = `${com.node_color_index[e.target]}`; t.hidden = false;
      e.color = `${com.edge_color_index[e.id]}`; e.hidden = false;
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
  exportGraphAsImage(params) {
    if(params.format=="svg") saveAsSVG(sigma_instance, {download: true}, params.mode);
    else saveAsPNG(sigma_instance, {download: true}, params.mode);
    
    
  },
  show_unconnectedGraph(state){
    var com = this;

    com.graph_state = state

    if(com.active_node) return

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
  edit_opacity: function() {
    var com = this;
    sigma_instance.graph.edges().forEach(function (e) {
      e.color = e.color.replace(/[\d.]+\)$/g, com.edge_opacity+')');
    });
    sigma_instance.refresh();
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
  async three_view() {
    var com = this;

    if(com.threeview) return;

    com.threeview = !com.threeview

    await this.wait(1);

    this.reset()

    sigma_instance.camera.goTo({ x: 0, y: 0, ratio: 1, angle: sigma_instance.camera.angle });
    sigma_instance.refresh()
    
    var threeGraphmod = document.getElementById('sigma-webgl')

    threeGraphmod.style.display = "flex"

    if(three_instance != null) {
      three_instance.resumeAnimation()
      return
    }

    var subgraphSet = new Set(com.gephi_data.subgraph)
    var newNodeList = Array.from(com.gephi_data.nodes.filter(node => subgraphSet.has(node.id)));

    const newEdges = Array.from(com.gephi_data.edges.filter(edge => 
    subgraphSet.has(edge.source) || subgraphSet.has(edge.target)));

    newEdges.forEach(edge => {
    edge.color = edge.color.replace("rgba", "rgb").replace(/,\s*\d?\.?\d+\s*\)/, ")");
    });


    // Random tree
    const gData = {
    nodes: newNodeList,
    links: newEdges
    };


    three_instance = ForceGraph3D();
    three_instance(threeGraphmod)
      .graphData(gData)
      .nodeLabel(node => `${node.label}`)
      .enableNodeDrag(false)
      .nodeAutoColorBy('group')
      .backgroundColor('rgb(0,0,0)')
      .linkWidth(2)
      .showNavInfo(false)
      .onNodeClick(node => this.activeNode(node));
       
  

      three_instance.refresh()
  },
  async two_view(){
    var com = this;

    var threeGraphmod = document.getElementById('sigma-webgl')
    var twoGraphmod = document.getElementById('sigma-canvas')
    threeGraphmod.style.display = "none"; twoGraphmod.style.display = "none"

    three_instance.pauseAnimation()
    
    com.threeview = !com.threeview
    await this.wait(1);

    document.getElementById('sigma-canvas').style.display = "flex"

    this.reset()

    sigma_instance.camera.goTo({ x: 0, y: 0, ratio: 1, angle: sigma_instance.camera.angle });
    sigma_instance.refresh()
    
  },
  async wait(ms) {
    return new Promise(resolve => {
      setTimeout(resolve, ms);
    });
  },
  update_boundary: function(data) {
    var com = this;

    var minBound = -data;
    var maxBound = data;

    sigma_instance.graph.edges().forEach(function (e) {
        // Nodes
        var source = sigma_instance.graph.getNodeFromIndex(e.source);
        var target = sigma_instance.graph.getNodeFromIndex(e.target);

        source.color = com.get_normalize(source.attributes[com.active_decoloumn], minBound, maxBound);
        target.color = com.get_normalize(target.attributes[com.active_decoloumn], minBound, maxBound);
        e.color = com.get_normalize(source.attributes[com.active_decoloumn], minBound, maxBound).replace(')', ', 0.2)').replace('rgb', 'rgba');

            
    });

    sigma_instance.refresh();
  },
  reset_node_label(node) {
    node.active = false
    node.sActive = false
    sigma_instance.refresh()
  },
  visualize_pathway(startID, endID){

    this.reset()
    const startNode = sigma_instance.graph.getNodeFromIndex(startID);
    const endNode = sigma_instance.graph.getNodeFromIndex(endID);
    const paths = new Set(sigma_instance.graph.astar(startNode.id, endNode.id));
    if(paths.size == 0) this.emitter.emit("emptySet", false);
    
    sigma_instance.graph.nodes().forEach(n =>{
      if(paths.has(n)){
        n.hidden = false;
        n.active = true
      } 
      else n.hidden = true;
    });

    sigma_instance.refresh()
  },

},
  mounted() {
    var com = this;

    //Initializing the sigma instance to draw graph network

    sigma_instance= new sigma();
    var camera = sigma_instance.addCamera();

    sigma_instance.addRenderer({
      container: "sigma-canvas",
      type: "canvas",
      camera: camera,
      settings: {
        defaultLabelColor: "#FFF",
        hideEdgesOnMove: true,
        minNodeSize: 1,
        maxNodeSize: 20,
        labelThreshold: 5,
      }
    });

    sigma_instance.graph.clear();
    sigma_instance.graph.read(com.gephi_data);
    

    com.edit_opacity()

    

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

    
    this.emitter.on("unconnectedGraph", state => {
      this.show_unconnectedGraph(state)
    });
    
    this.emitter.on("searchNode", state => {
      this.$emit('active_node_changed', sigma_instance.graph.getNodeFromIndex(state.id))
    });
    this.emitter.on("searchPathway", element => {
      this.visualize_pathway(element.source, element.target)
    });
    
    this.emitter.on("searchSubset", state => {
      this.$emit('active_subset_changed', state)
    });

    this.emitter.on("searchEnrichment", state => {
      this.$emit('active_term_changed', state)
    });

    this.emitter.on("highlightProteinList", state => {
      this.$emit('subactive_subset_changed', state)
    });

    this.emitter.on("hideTermLayer", state => {
      this.colorpalette = this.$store.state.colorpalette
      this.$emit('active_termlayers_changed', state)
    });

    this.emitter.on("hideSubset", state => {
      this.$emit('active_layer_changed', state)
    });
    
    this.emitter.on("centerGraph", () => {
      sigma_instance.camera.goTo({ x: 0, y: 0, ratio: 1, angle: sigma_instance.camera.angle });
    });
    
    this.emitter.on("exportGraph", (params) => {
      this.exportGraphAsImage(params)
    });

    this.emitter.on("resetSelect", () => {
      this.reset_label_select()
    });

    this.emitter.on("hideLabels", (state) => {
      this.hide_labels(state)
    });

    this.emitter.on("threeView", () => {
      this.three_view()
    });
    this.emitter.on("adjustDE", (value) => {
      this.update_boundary(value)
    });
    
    sigma_instance.refresh()


  },
  activated() {
    sigma_instance.refresh()
  }
}
</script>

<style>

.visualization {
  display: flex;
  width: 100%;

}
#sigma-webgl{
position: absolute;
display: none;
width: 0;
height: 0;
}


#sigma-canvas {

  position: absolute;
  box-sizing: border-box;
  overflow: hidden;
  background-color: hsla(0,0%,100%,.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

#sigma-canvas.loading {

border-radius: 30px;
border-style: solid;
border-color: white;
top: 50%;
left: 0;
width: 450px;
height: 350px;
position: absolute;
background-color: hsla(0,0%,100%,.05);
backdrop-filter: blur(10px);
-webkit-backdrop-filter: blur(10px);
}

#threeview {
  position: absolute;
  z-index: 999;
}

.twoview {
  right: 0;
  position: absolute;
  margin: 10px;
  width: 20px;
  z-index: 999;
  transition: width 0.2 ease-in;
}

.twoview:hover {
  width: 25px;
  transition: width 0.2 ease-in;
}

.sigma-label {
color: #fff; /* set the font color to white */
}
</style>
  
  