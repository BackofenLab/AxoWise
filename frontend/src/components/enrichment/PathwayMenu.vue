<template>
    <div class="pathways" :class="{ show_pathways_menu: pane_hidden === true }">
        <div class="minimize-bar" v-on:click="print()" >
            <img src="@/assets/pathwaybar/arrows.png" :style="{ transform: pane_hidden ? 'rotate(-90deg)' : 'rotate(90deg)' }">
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
    data() {
        return {
            pane_hidden: false
        }
    },
    methods: {
        print() {
            console.log("hello")
            this.pane_hidden = !this.pane_hidden
        }
        
      
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
        background: #D9D9D9;
        text-align: center;
    }
    .minimize-bar img {
        width: 0.84%;
        height: 55.56%;
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
    }

</style>