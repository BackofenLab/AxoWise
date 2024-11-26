<template>
    <div class="visualization">
        <div id="sigma-canvas" ref="container" class="sigma-parent"></div>
    </div>
</template>

<script>
import Sigma from "sigma";
import { NodeBorderProgram } from "@sigma/node-border";
import { drawHover, drawLabel } from "./utils/canvas-utils";

export default {
name: "GraphContainer",
props: ["graph"],
mounted() {
    
    this.sigmaInstance = new Sigma(this.graph, this.$refs.container, {
        defaultNodeType: "bordered",
        nodeProgramClasses: {
        bordered: NodeBorderProgram,
        },
    });

    // this.sigmaInstance.setSetting("labelColor", {color:'#FFF'})
    this.sigmaInstance.setSetting("defaultDrawNodeLabel", drawLabel)
    this.sigmaInstance.setSetting("defaultDrawNodeHover", drawHover)
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
</style>
