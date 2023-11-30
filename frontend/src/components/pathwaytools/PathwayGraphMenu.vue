<template>
    <div class="pathways" :class="{ show_pathways_menu: pane_hidden === true }">
        <div class="minimize-bar" v-on:click="pane_hidden = !pane_hidden" >
            <img src="@/assets/pathwaybar/arrows.png" :style="{ transform: pane_hidden ? 'rotate(-90deg)' : 'rotate(90deg)' }">
        </div>
        <div class="pathwaybar" v-show="pane_hidden === false">
            <PathwayGraphList
            :term_data='term_data'
            ></PathwayGraphList>
            <PathwayGraphGraphs
            :gephi_data='gephi_data'
            :filtered_terms='filtered_terms'
            :favourite_pathways='favourite_pathways'
            ></PathwayGraphGraphs>
            <img id="pathway-bg" src="@/assets/pathwaybar/background-dna.png">
        </div>
    </div>
</template>

<script>
import PathwayGraphList from '@/components/pathwaytools/PathwayGraphList.vue'
import PathwayGraphGraphs from '@/components/pathwaytools/PathwayGraphGraphs.vue'

export default {
    name: 'PathwayMenu',
    props: ['term_data','active_term'],
    components: {
        PathwayGraphList,
        PathwayGraphGraphs
    },
    data() {
        return {
            pane_hidden: false,
        }
    },
    mounted() {
    },
}
</script>


<style>
</style>