<template>
    <div class="visualization">
        <div id="sigma-canvas" ref="container" class="sigma-parent"></div>
    </div>
</template>

<script>
import Sigma from "sigma";
import { NodeBorderProgram } from "@sigma/node-border";
import { drawHover, drawLabel } from "./utils/canvas-utils";
import { nodeReducer, edgeReducer } from './utils/basic-reducer';
import { generateCluster } from './utils/cluster';

export default {
name: "GraphContainer",
props: ["graph"],
data(){
    return {
        state: {}
    }
},
mounted() {
    let com = this;
    
    com.renderer = new Sigma(this.graph, this.$refs.container, {
        defaultNodeType: "bordered",
        nodeProgramClasses: {
        bordered: NodeBorderProgram,
        },
    });

    com.renderer.setSetting("defaultDrawNodeLabel", drawLabel)
    com.renderer.setSetting("defaultDrawNodeHover", drawHover)
    com.renderer.setSetting("nodeReducer", (node, data) => {
    return nodeReducer(node, data, com.state);
    });
    com.renderer.setSetting("edgeReducer", (edge, data) => {
    return edgeReducer(com.graph, edge, data, com.state);
    });

    generateCluster( "sigma-canvas", com.renderer, com.graph);


    /* Event handling functions call.
       Events: ['enterNode','leaveNode','clickNode']
    */
    com.renderer.on("enterNode", ({ node }) => {
    com.setHoveredNode(node);
    });
    com.renderer.on("leaveNode", () => {
    com.setHoveredNode(undefined);
    });
    com.renderer.on("clickNode", ({ node }) => {
    com.setClickedNode(node);
    });

},
methods: {
    /**
     * Sets the currently hovered node and its neighbors in the component's state.
     * Updates the rendering to reflect the changes.
     *
     * @param {string|null|undefined} node - The ID of the node to set as hovered.
     * If `null` or `undefined`, clears the hovered node and its neighbors.
     */
    setHoveredNode(node) {
    let com = this;

    if (node) {
    com.state.hoveredNode = node;
    com.state.hoveredNeighbors = new Set(com.graph.neighbors(node));
    }

    if (!node) {
    com.state.hoveredNode = undefined;
    com.state.hoveredNeighbors = undefined;
    }
    // Refresh rendering
    com.renderer.refresh({
    skipIndexation: true,
    });
    },

    /**
    * Sets the currently clicked node and its neighbors in the component's state.
    * Updates the rendering to reflect the changes.
    *
    * @param {string|null|undefined} node - The ID of the node to set as clicked.
    * If `null` or `undefined`, clears the clicked node and its neighbors.
    */
    setClickedNode(node) {
    let com = this;

    if (node) {
    com.state.clickedNode = node;
    com.state.clickedNeighbors = new Set(com.graph.neighbors(node));
    }

    // Refresh rendering
    com.renderer.refresh({
    skipIndexation: true,
    });
  }
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
    pointer-events: auto
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
