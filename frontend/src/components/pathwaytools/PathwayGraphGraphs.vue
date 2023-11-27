<template>
    <div id="pathways-graphs">
        <div id="pathway-tools-filter" class="colortype">
            <span>{{ tool }}</span>
        </div>
        <div class="graph-section colortype">
            <PathwayGraph v-show="tool == 'Termgraph'"
            :term_data='term_data'
            :mode = 'mode'
            :filtered_terms = 'filtered_terms'
            :bookmark_off = 'bookmark_off'
            ></PathwayGraph>
        </div>
    </div>
</template>

<script>

import PathwayGraph from '@/components/enrichment/graph/PathwayGraph.vue'

export default {
    name: 'PathwayGraphGraphs',
    props: ['term_data','filtered_terms'],
    components: {
        PathwayGraph,
    },
    data() {
        return {
            tool: 'Termgraph',
            favourite_graphs: new Set(),
            bookmark_off: true,
            tool_selecting: false,
            mode: 'term',
            tools: [{id: 'Termgraph'}]
        }
    },
    methods: {
    },
}
</script>


<style>
    #pathways-graphs {
        width: 50.92%;
        height: 96.92%;
        position: absolute;
        top:50%;
        transform: translateY(-50%);
        margin-left: 48.74%;
        border-radius: 10px;
        z-index: 999;
        font-family: 'ABeeZee', sans-serif;
    }
</style>