<template>
    <div id="pathways">
        <div class="minimize-bar">
            <img src="@/assets/pathwaybar/arrows.png">
        </div>
        <div class="pathwaybar">
            <PathwayList></PathwayList>
            <PathwayGraph></PathwayGraph>
            <img id="pathway-bg" src="@/assets/pathwaybar/background-dna.png">
        </div>
    </div>
</template>

<script>
import PathwayList from '@/components/enrichment/PathwayList.vue'
import PathwayGraph from '@/components/enrichment/PathwayGraph.vue'

export default {
    name: 'PathwayMenu',
    components: {
        PathwayList,
        PathwayGraph
    },
}
</script>


<style>
    #pathways {
        z-index: 999;
    }
    .minimize-bar {
        width: 92.97%;
        height: 2.5%;
        position: fixed;
        top: 70.7%;
        left: 50%;
        flex-shrink: 0;
        transform: translateX(-50%);
        border-radius: 10px 10px 0px 0px;
        background: #D9D9D9;
        text-align: center;
    }
    .minimize-bar img {
        width: 0.84%;
        height: 55.56%;
        transform: rotate(90deg);
        flex-shrink: 0;
    }
    .pathwaybar {
        width: 92.97%;
        height: 24.07%;
        position: fixed;
        top: 73.2%;
        left: 50%;
        flex-shrink: 0;
        transform: translateX(-50%);
        border-radius: 0px 0px 10px 10px;
        background: rgba(222, 222, 222, 0.61);
        backdrop-filter: blur(7.5px);
        overflow: hidden;
    }
    .pathwaybar #pathway-bg {
        width: 20%;
        height: 100%;
        margin-left: 30.87%;
        position: fixed;
        top:50%;
        transform: translateY(-50%);
    }
</style>