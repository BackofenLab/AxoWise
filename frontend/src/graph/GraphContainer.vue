<template>
    <div class="visualization">

        <div id="sigma-canvas" ref="container" class="sigma-parent"></div>
    </div>
</template>

<script>
import Sigma from "sigma";

export default {
name: "GraphContainer",
props: ["graph"],
mounted() {
    
    console.log("container",this.graph)
    this.sigmaInstance = new Sigma(this.graph, this.$refs.container);
    console.log("container2",this.sigmaInstance)

    // Example: Add any additional customizations or styles
    // this.sigmaInstance.getRenderer().setSettings({
    // defaultNodeColor: "#ff5722",
    // defaultEdgeColor: "#999999",
    // });
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
