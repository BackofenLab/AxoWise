<template>
    <div id="pathways-graphs">
        <img src="@/assets/pathwaybar/pathway-button.png">
        <div class="graph-section"></div>
    </div>
</template>

<script>

export default {
    name: 'PathwayGraphs',
    
}
</script>


<style>
    #pathways-graphs {
        width: 50.92%;
        height: 96.92%;
        position: fixed;
        top:50%;
        transform: translateY(-50%);
        margin-left: 48.74%;
        border-radius: 10px;
        z-index: 999;
    }
    #pathways-graphs img {
        width: 24.20%;
        height: 11.16%;
        position: fixed;
    }
    .graph-section {
        width: 100%;
        height: 87.65%;
        top: 12.35%;
        border-radius: 10px;
        background: #0A0A1A;
        position: fixed;
    }
</style>