<template>
    <div class="pathways" :class="{ show_pathways_menu: pane_hidden === true }">
        <div class="minimize-bar" v-on:click="pane_hidden = !pane_hidden" >
            <img src="@/assets/pathwaybar/arrows.png" :style="{ transform: pane_hidden ? 'rotate(-90deg)' : 'rotate(90deg)' }">
        </div>
        <div class="pathwaybar">
            <PathwayList
            :gephi_data='gephi_data'
            ></PathwayList>
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
    props: ['gephi_data','active_term'],
    components: {
        PathwayList,
        PathwayGraph
    },
    data() {
        return {
            pane_hidden: false
        }
    },
    methods: {
         
        }
    }
</script>


<style>
    .pathways {
        z-index: 999;
        position: fixed;
        width: 92.97%;
        height: 27.2%;
        top: 70.7%;
        left: 50%;
        transform: translateX(-50%);
        transition: transform 330ms ease-in-out;
    }
    .minimize-bar {
        width: 100%;
        height: 9.41%;
        position: fixed;
        flex-shrink: 0;
        border-radius: 10px 10px 0px 0px;
        backdrop-filter: blur(7.5px);
        background: #D9D9D9;
        text-align: center;
    }
    .minimize-bar img {
        width: 0.7vw;
        height: 0.7vw;
        flex-shrink: 0;
        transition: transform 330ms ease-in-out;
    }
    .pathwaybar {
        width: 100%;
        height: 90.59%;
        position: fixed;
        top: 9.41%;
        flex-shrink: 0;
        border-radius: 0px 0px 10px 10px;
        background: rgba(222, 222, 222, 0.61);
        backdrop-filter: blur(7.5px);
    }
    .pathwaybar #pathway-bg {
        width: 20%;
        height: 100%;
        margin-left: 30.87%;
        position: absolute;
        top:50%;
        transform: translateY(-50%);
    }
    .show_pathways_menu {
        transform: translate(-50%,98%);
        width: 20%;
        transition: transform 330ms ease-in-out;
        transition: width 900ms ease-in-out;
    }

</style>