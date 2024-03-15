<template>
    <div id="pathways-graphs">
        <div class="tool-section-term">
            <div class="generate" v-show="tool == 'Termgraph'">
                <div class="generate-text" v-on:click="get_term_graph()">generate graph</div>
            </div>
            <div class="generate" :class="{recolor_filter: bookmark_off == false}" v-on:click="bookmark_off = !bookmark_off">
                <div class="generate-text" >bookmarks</div>
            </div>
        </div>
        <div class="graph-section">
            <PathwayGraph v-show="tool == 'Termgraph'"
            :mode = 'mode'
            :gephi_data='gephi_data'
            :filtered_terms = 'filtered_terms'
            :bookmark_off = 'bookmark_off'
            ></PathwayGraph>
        </div>
    </div>
</template>

<script>

import PathwayGraph from '@/components/enrichment/graph/PathwayGraph.vue'

export default {
    name: 'PathwayTools',
    props: ['gephi_data','filtered_terms', 'favourite_pathways'],
    components: {
        PathwayGraph,
    },
    data() {
        return {
            tool: 'Termgraph',
            favourite_graphs: new Set(),
            bookmark_off: true,
            tool_selecting: false,
            mode: 'protein',
            tools: [{id: 'Termgraph'}, {id: 'Heatmap'}]
        }
    },
    methods: {
        get_term_graph(){
            this.emitter.emit("generateGraph");
        },

    },
}
</script>


<style>
    #pathways-graphs {
        width: 100%;
        height: 100%;
        z-index: 999;
        font-family: 'ABeeZee', sans-serif;
    }
    .generate {
        width: 50%;
        cursor: default;
        background: #D9D9D9;
    }
    .generate .generate-text {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0A0A1A;
        font-size: 0.7vw;
    }

    .export-heatmap {
        position: absolute;
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
        background: #D9D9D9;
        width: 2.5vw;
        align-content: center;
        justify-content: center;
    }

    #pathway-tools-filter {
        width: 17.81%;
        height: 11.16%;
        display: flex;
        position: absolute;
        border-radius: 5px;
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

    .tool-section-term {
        display: inline-flex;
        margin: 1vw 0 1vw 0;
        height: 1vw;
        width: 100%;
        align-items: center;
        justify-content: center;
    }

</style>