<template>
    <div class="visualization">
      <div id="sigma-canvas" ref="container" class="sigma-parent"></div>
    </div>
  </template>
  
  <script>
  import { useVisualizationStore } from "@/store/ProteinStore";
  import Sigma from "sigma";
  import { NodeBorderProgram } from "@sigma/node-border";
  import { drawHover, drawLabel } from "./utils/canvas-utils";
  import { nodeReducer, edgeReducer } from "./utils/basic-reducer";
  import { generateCluster } from "./utils/cluster";
  
  export default {
    name: "GraphContainer",
    props: ["graph"],
    setup() {
      const store = useVisualizationStore();
      return { store };
    },
    mounted() {
      const com = this;
  
      com.renderer = new Sigma(this.graph, this.$refs.container, {
        defaultNodeType: "bordered",
        nodeProgramClasses: {
          bordered: NodeBorderProgram,
        },
      });

      const { store } = this;
      store.setRenderer(com.renderer);
      store.setGraph(com.graph);
  
      com.renderer.setSetting("defaultDrawNodeLabel", drawLabel);
      com.renderer.setSetting("defaultDrawNodeHover", drawHover);
      com.renderer.setSetting("nodeReducer", (node, data) => {
        return nodeReducer(node, data, store);
      });
      com.renderer.setSetting("edgeReducer", (edge, data) => {
        return edgeReducer(com.graph, edge, data, store);
      });
  
      generateCluster("sigma-canvas", com.renderer, com.graph);
  
      /** 
       * Event handling functions call.
       * Events: ['clickNode']
       */
      com.renderer.on("clickNode", ({ node }) => {
        store.setClickedNode(node, com.graph);
      });
  
      /* 
       * Emit handling functions.
       * Events: ['searchEnrichment']
       */
      this.emitter.on("searchEnrichment", (enrichment) => {
        store.setClickedEnrichment(enrichment.symbols);
      });
    },
    beforeUnmount() {
      if (this.sigmaInstance) {
        this.sigmaInstance.kill();
      }
    },
  };
  </script>
  
  <style>
  #sigma-canvas {
    position: absolute;
    height: 100%;
    width: 80%;
    left: 20%;
    box-sizing: border-box;
    overflow: hidden;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }
  #clustersLayer {
    width: 100%;
    height: 100%;
    position: absolute;
    pointer-events: auto;
  }
  .clusterLabel {
    position: absolute;
    transform: translate(-50%, -50%);
    font-family: sans-serif;
    font-variant: small-caps;
    font-weight: 400;
    font-size: 1rem;
    opacity: 100%;
  }
  .clusterCircle {
    position: absolute;
    border-radius: 50%;
    opacity: 20%;
  }
  </style>
  