<template>
    <div id="pathways-graphs">
        <div id="pathway-tools-filter" v-on:click="handling_filter_menu()" >
            <span>{{ tool }}</span>s
        </div>
        <div id="pathway-tools-filter-categories" v-show="tool_selecting== true">
            <div class="element" v-for="(entry, index) in tools" :key="index" v-on:click="tool = entry.id; handling_filter_menu()">
                <a>{{ entry.id }}</a>
            </div>
        </div>
        <div class="generate" v-show="tool == 'Termgraph'">
            <div class="generate-text" v-on:click="get_term_graph()">Generate term graph</div>
        </div>
        <div class="generate" v-show="tool == 'Heatmap'">
            <div class="generate-text" v-on:click="get_heatmap()">Generate heatmap</div>
        </div>
        <div class="bookmark-button-graph" v-on:click="bookmark_off = !bookmark_off">
            <img class="bookmark-image" src="@/assets/pathwaybar/favorite.png" :class="{recolor_filter: bookmark_off == false}">
        </div>
        <div class="graph-section">
            <PathwayGraph v-show="tool == 'Termgraph'"
            :terms = 'terms'
            :bookmark_off = 'bookmark_off'
            ></PathwayGraph>
            <PathwayHeatmap v-show="tool == 'Heatmap'"
            :bookmark_off = 'bookmark_off'
            :favourite_pathways = 'favourite_pathways'
            ></PathwayHeatmap>
        </div>
    </div>
</template>

<script>

import PathwayGraph from '@/components/enrichment/graph/PathwayGraph.vue'
import PathwayHeatmap from '@/components/enrichment/heatmap/PathwayHeatmap.vue'

export default {
    name: 'PathwayTools',
    props: ['terms', 'favourite_pathways'],
    components: {
        PathwayGraph,
        PathwayHeatmap
    },
    data() {
        return {
            tool: 'Termgraph',
            favourite_graphs: new Set(),
            bookmark_off: true,
            tool_selecting: false,
            tools: [{id: 'Termgraph'}, {id: 'Heatmap'}]
        }
    },
    methods: {
        get_term_graph(){
            this.emitter.emit("generateGraph");
        },
        get_heatmap(){
            this.emitter.emit("generateHeatmap");
        },
        handling_filter_menu() {
            var com = this;
            if (!com.tool_selecting) {
                com.tool_selecting = true;

                // Add the event listener
                document.addEventListener('mouseup', com.handleMouseUp);
            }
            else{
                com.tool_selecting = false;
                document.removeEventListener('mouseup', com.handleMouseUp);
            }

        },
        handleMouseUp(e) {
            var com = this;

            var container = document.getElementById('pathway-tools-filter-categories');
            var container_button = document.getElementById('pathway-tools-filter');
            if (!container.contains(e.target) && !container_button.contains(e.target)) {
                com.tool_selecting = false;

                // Remove the event listener
                document.removeEventListener('mouseup', com.handleMouseUp);
            }
        }
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