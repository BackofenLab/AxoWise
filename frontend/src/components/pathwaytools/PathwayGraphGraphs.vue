<template>
    <div id="pathways-graphs">
        <div id="pathway-tools-filter">
            <span>{{ tool }}</span>
        </div>
        <div class="graph-section">
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
    .generate {
        width: 24.20%;
        height: 11.16%;
        left: 18.51%;
        position: absolute;
        border-radius: 5px;
        background: #0A0A1A;
        cursor: default;
    }
    .generate .generate-text {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.95vw;
    }

    .export-heatmap {
        width: 24.20%;
        height: 11.16%;
        left: 48.92%;
        position: absolute;
        border-radius: 5px;
        background: #0A0A1A;
        cursor: default;
    }

    .export-heatmap .generate-text {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.95vw;
    }

    .bookmark-button-graph {
        width: 4.81%;
        height: 11.16%;
        left: 43.41%;
        position: absolute;
        border-radius: 5px;
        background: #0A0A1A;
        align-content: center;
        justify-content: center;
    }

    #pathway-tools-filter {
        width: 17.81%;
        height: 11.16%;
        display: flex;
        position: absolute;
        border-radius: 5px;
        background: #0A0A1A;
        align-items: center;
        justify-content: center;
    }

    #pathway-tools-filter span {
        display: block;
        width: 90%;
        font-size: 0.95vw;
        color: white;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        cursor: default;
        text-align: center;
    }

    #pathway-tools-filter-categories {
        display: flex;
        position: fixed;
        width: 20%;
        height: 30.32%;
        left: -1.5%;
        top: 15%;
        padding: 1% 0% 1% 0%;
        border-radius: 5px;
        border: 1px solid #FFF;
        background: #0A0A1A;
        z-index: 1;
        justify-content: center;
        overflow-x: scroll;
        overflow-y: hidden;
        cursor: default;
    }

    #pathway-tools-filter-categories .element {
        border-radius: 5px;
        background: rgba(217, 217, 217, 0.17);
        display: flex;
        width: 36.88%;
        height: 100%;
        margin: 0% 2% 0% 2%;
        overflow: hidden;

    }
    #pathway-tools-filter-categories .element:hover {
        background: rgba(217, 217, 217, 0.47);
    }
</style>