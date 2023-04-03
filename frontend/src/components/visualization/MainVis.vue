<template>
    <div id="sigma-webgl" ref="sigmaContainer" @contextmenu.prevent="handleSigmaContextMenu">
    </div>
  </template>

<script>
import sigma from "sigma";
import Graph from 'graphology'
import {scaleLinear} from "d3-scale";
import saveAsPNG from '../../rendering/saveAsPNG';

var sigma_instance = null;

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
      state: null
    }
  },
  watch: {
    gephi_data(){
      const com = this

      const graph = new Graph();
      com.gephi_data.nodes.forEach(node => {
        var { id, x, y, color, size, label, attributes, hidden } = node;
        size = size*0.4
        graph.addNode(id, { x, y, color, size, label, attributes, hidden});
      });

      com.gephi_data.edges.forEach(edge => {
        var { id, source, target, attributes, color } = edge;
        color = color.replace(/rgba/g, 'rgb').replace(/,[^,)]*\)/g, '').replace(/\(\d+,\d+,\d+/g, '$&)')
        graph.addEdge(source, target, { id, source, target, attributes, color});
      });

      sigma_instance.setGraph(graph)
      
      sigma_instance.refresh();

    },
    active_node(node) {
      var com = this;

      com.reset()

      if(node == null) return

      const neighbors = new Set();
      const edges = sigma_instance.graph.edges()
      
      sigma_instance.graph.getNodeAttributes(node.attributes["Ensembl ID"]).color = "rgb(255, 255, 255)"

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

      graph.nodes().forEach(function (n) {
        var node = graph.getNodeAttributes(n);
        if (proteins.has(n)) {
          node.color = "rgb(255, 255, 255)"
        } else {
          node.color = "rgb(0, 100, 0)"
        }
      });

      graph.edges().forEach(function (e) {
        const edge = sigma_instance.graph.getEdgeAttributes(e)
        const source = graph.getNodeAttributes(edge.source);
        const target = graph.getNodeAttributes(edge.target);
        const source_present = proteins.has(source.attributes["Ensembl ID"]);
        const target_present = proteins.has(target.attributes["Ensembl ID"]);

        if (source_present && !target_present || !source_present && target_present) {
          edge.color = "rgb(220, 255, 220)"
        } else if (source_present && target_present) {
          edge.color = "rgb(255, 255, 255)"
        } else {
          edge.color = "rgb(0, 100, 0)"
        }
      });

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
        const edgeAttrs = graph.getEdgeAttributes(edge);
        const sourceNode = graph.getNodeAttributes(edgeAttrs.source);
        const targetNode = graph.getNodeAttributes(edgeAttrs.target);
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
          edgeAttrs.color = sourcePresent && !targetPresent ? "rgba(200, 255, 255)" : "rgba(0, 100, 100)";
        } else {
          edgeAttrs.color = sourcePresent ? "rgba(255, 255, 255)" : "rgba(0, 100, 100)";
        }
      }
      this.$store.commit('assign_graph_subset', sigma_instance.graph)
      sigma_instance.refresh();
    },
    active_layer(layer) {

      const graph = sigma_instance.graph;

      if(layer == null){
        graph.nodes().forEach(function (n) {
          var node = graph.getNodeAttributes(n);
            node.hidden = false;
        });
        sigma_instance.refresh()
        return
      }

      var proteins = new Set(layer);

      graph.nodes().forEach(function (n) {
        var node = graph.getNodeAttributes(n);
        if (proteins.has(n)) {
          node.hidden = false;
        } else {
          node.hidden = true;
        }
      });
    
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
        const edgeAttrs = graph.getEdgeAttributes(edge);
        const sourceNode = graph.getNodeAttributes(edgeAttrs.source);
        const targetNode = graph.getNodeAttributes(edgeAttrs.target);
        const source_value = sourceNode.attributes[com.active_decoloumn];
        const target_value = targetNode.attributes[com.active_decoloumn];

        sourceNode.color = com.get_normalize(source_value, -1, 1);
        targetNode.color = com.get_normalize(target_value, -1, 1);
        edgeAttrs.color = com.get_normalize(source_value, -1, 1);

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
      const edge = sigma_instance.graph.getEdgeAttributes(e);
      const s = sigma_instance.graph.getNodeAttributes(edge.source);
      const t = sigma_instance.graph.getNodeAttributes(edge.target);
      s.color = `${com.node_color_index[edge.source]}`; s.hidden = false;
      t.color = `${com.node_color_index[edge.target]}`; t.hidden = false;
      edge.color = `${com.edge_color_index[edge.id]}`; edge.hidden = false;
    });

    if(com.state == "Main Graph" || com.state == null ) {
      com.unconnected_nodes.forEach(function (n) {
        var node = sigma_instance.graph.getNodeAttributes(n.id);
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
  handleSigmaContextMenu(event) {
    if(!this.isSelecting){
      this.isSelecting = true;
        this.startX = event.x; this.startY = event.y;
         // Create a new selection box element
        this.selectionBox = document.createElement('div');
        this.selectionBox.style.position = 'absolute';
        this.selectionBox.style.border = '1px solid #fff';
        this.selectionBox.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
        this.selectionBox.style.zIndex = '100';
        this.selectionBox.style.pointerEvents = 'none';

        // Add the selection box element to the container
        this.$refs.sigmaContainer.appendChild(this.selectionBox);

        // Set the initial position of the selection box
        this.selectionBox.style.left = `${this.startX}px`; this.selectionBox.style.top = `${this.startY}px`;
        this.selectionBox.style.width = '0'; this.selectionBox.style.height = '0';

        return
      }

      if (this.isSelecting) {
        this.isSelecting = false

        this.endX = event.x; this.endY = event.y;

        this.$refs.sigmaContainer.removeChild(this.selectionBox); this.selectionBox = null;
        // Get all nodes within the selection rectangle

        
        const nodesInRectangle = sigma_instance.graph.nodes().filter(node => {
          const nodeAttr = sigma_instance.graph.getNodeAttributes(node)
          const nodeX = nodeAttr.x; const nodeY = nodeAttr.y;
          const screen = sigma_instance.graphToViewport({ x: nodeX, y: nodeY })
          const screenX = screen.x; const screenY = screen.y
          const startX = Math.min(this.startX, this.endX); const endX = Math.max(this.startX, this.endX);
          const startY = Math.min(this.startY, this.endY); const endY = Math.max(this.startY, this.endY);
          return (screenX >= startX && screenX <= endX && screenY >= startY && screenY <= endY);
        });
        
        // Do something with the selected nodes
        const node_attributes_list = nodesInRectangle.map(node_id => sigma_instance.graph.getNodeAttributes(node_id)); 

        this.$emit('active_subset_changed', node_attributes_list)
     }

    },
    handleMouseMove(event) {
      if(this.isSelecting){
        this.endX = event.x; this.endY = event.y;

        const position = {
        x: Math.min(this.startX, this.endX),
        y: Math.min(this.startY, this.endY)};

        const width = Math.abs(this.endX - this.startX); const height = Math.abs(this.endY - this.startY);
        this.selectionBox.style.left = `${position.x}px`; this.selectionBox.style.top = `${position.y}px`;
        this.selectionBox.style.width = `${width}px`; this.selectionBox.style.height = `${height}px`;
      }
    },
    exportGraphAsImage() {
      // Get a reference to your Sigma.js container element
      const layers = ["edges", "nodes", "edgeLabels", "labels"]
      saveAsPNG(sigma_instance, layers)
      
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
          var node = graph.getNodeAttributes(n.id);
          node.hidden = false
        });
        sigma_instance.refresh();
      }
      
      if(state == "Main Graph"){
        com.unconnected_nodes.forEach(function (n) {
          var node = graph.getNodeAttributes(n.id);
          node.hidden = true
        });
        sigma_instance.refresh();
      }

      
  },
},
  mounted() {
    var com = this;

    //Initializing the sigma instance to draw graph network
    const graph = new Graph();
    com.gephi_data.nodes.forEach(node => {
      var { id, x, y, color, size, label, attributes, hidden } = node;
      size = size*0.4
      graph.addNode(id, { x, y, color, size, label, attributes, hidden});
    });

    com.gephi_data.edges.forEach(edge => {
      var { id, source, target, attributes, color } = edge;
      color = color.replace(/rgba/g, 'rgb').replace(/,[^,)]*\)/g, '').replace(/\(\d+,\d+,\d+/g, '$&)')
      graph.addEdge(source, target, { id, source, target, attributes, color});
    });

    const container = document.getElementById("sigma-webgl")
    const settings = {
        labelColor: {color: '#fff'},
      }

    sigma_instance = new sigma(graph, container, settings);

    sigma_instance.on('clickNode',(event) => {
      this.activeNode(sigma_instance.graph.getNodeAttributes(event.node))
    });

    sigma_instance.mouseCaptor.on('mousemove',(event) => {
      com.handleMouseMove(event)
    });

    this.emitter.on("exportGraph", nameGraph => {
      this.exportGraphAsImage()
      console.log(nameGraph)
    });

    this.emitter.on("unconnectedGraph", state => {
      this.show_unconnectedGraph(state)
    });

    this.emitter.on("searchNode", state => {
      this.$emit('active_node_changed', state)
    });

    this.emitter.on("centerGraph", () => {
      sigma_instance.camera.setState({ x: 0.5, y: 0.5, ratio: 1, angle: 0 });
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

  .sigma-label {
  color: #fff; /* set the font color to white */
  }
</style>
  
  