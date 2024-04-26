<template>
    <div class="slider" tabindex="0">
        <span v-if="term_graphs.size == 0">There is no generated pathway graph.</span>
        <div v-for="(entry, index) in filt_graphs" :key="index" class="graph" v-on:click="switch_graph(entry)" @mouseover="activeGraphIndex = index" @mouseout="activeGraphIndex = -1">
            <SnapshotGraph :propValue="entry" :index="entry.id"/>
            <div class="graph-options" >
                <div class="bookmark-graph"  v-show="activeGraphIndex == index"  v-on:click.stop="add_graph(entry)" :class="{ checked: favourite_graphs.has(entry.id)}" ref="checkboxStatesGraph"></div>
                <img  class="remove-graph" v-show="activeGraphIndex == index" src="@/assets/pathwaybar/cross.png" v-on:click.stop="remove_graph(entry)">
                <div class="graph-name">
                    <input type="text" v-model="entry.label" class="empty" @click.stop />
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import SnapshotGraph from '@/components/enrichment/graph/SnapshotGraph.vue'

export default {
    name: 'PathwayGraphs',
    props: ['gephi_data','filtered_terms', 'bookmark_off','mode'],
    emits: ['loading_state_changed'],
    components: {
        SnapshotGraph,
    },
    data() {
        return {
            api: {
                termgraph: "api/subgraph/terms",
            },
            term_graphs: [],
            term_graphs_array: [],
            favourite_graphs: new Set(),
            activeGraphIndex: -1,
            graph_number: -1,
            species: null
        }
    },
    mounted(){
        if(this.mode !='term') {
            this.emitter.on("generateGraph", (set) => {
                this.get_term_data(set)
            });
        }
        this.term_graphs_array = this.$store.state.term_graph_dict
        if(this.term_graphs_array.length != 0) {
            this.graph_number = Math.max.apply(Math, this.term_graphs_array.map(item => item.id))
            this.term_graphs = new Set(this.term_graphs_array)
        }
        else{
            this.term_graphs = new Set()
        }
        
    },
    beforeUnmount () {
        this.emitter.off('generateGraph')
    },
    activated(){
        console.log("activated")
            this.term_graphs = new Set(this.$store.state.term_graph_dict)
            this.favourite_graphs = this.$store.state.favourite_graph_dict
    },
    methods: {
        get_term_data(set) {
            var com = this

            var formData = new FormData()
            if(!set)formData.append('func-terms', JSON.stringify(com.filtered_terms))
            else formData.append('func-terms', JSON.stringify(set))
            formData.append('species_id', com.gephi_data.nodes[0].species);

            this.axios
                .post(com.api.termgraph, formData)
                .then((response) => {
                    if(response.data){
                        this.graph_number += 1
                        if(this.term_graphs.size < 1) {
                            this.$store.commit('assign_term_graph', {id: this.graph_number, graph: response.data})
                        }
                        this.$store.commit('assign_new_term_graph', {id: this.graph_number, label: `Graph ${this.graph_number}`, graph: response.data})
                        this.term_graphs.add({ id: this.graph_number, label: `Graph ${this.graph_number}`, graph: response.data});
                        com.$emit("loading_state_changed", false);
                    }
                })

        },
        switch_graph(entry) {
            this.$store.commit('assign_term_graph', {id: entry.id, graph: entry.graph})
            if(this.mode == 'term') this.emitter.emit('graphChanged')
            else this.$router.push("terms")

        },
        remove_graph(entry) {
            if (!this.favourite_graphs.has(entry.id)) {
                // Checkbox is checked, add its state to the object
                this.favourite_graphs.delete(entry.id)
                this.$store.commit('assign_favourite_graph', this.favourite_graphs)
            }
            this.term_graphs.delete(entry)
            this.$store.commit('remove_snapshotPathway', entry.id)
            this.$store.commit('remove_term_graph', entry)
            if(![...this.term_graphs].some(e => e.id == this.$store.state.term_graph_data.id)) {
                this.$store.commit('assign_term_graph', null)
            }
        },
        add_graph(entry){
            if (!this.favourite_graphs.has(entry.id)) {
                this.favourite_graphs.add(entry.id)
            } else {
                this.favourite_graphs.delete(entry.id)
            }
            this.$store.commit('assign_favourite_graph', this.favourite_graphs)
        },
    },
    computed: {
        filt_graphs() {
            var com = this;
            var filtered = [...com.term_graphs];

            if (!com.bookmark_off){
                filtered = filtered.filter(function(term) {
                    return com.favourite_graphs.has(term.id)
                });
            }

            return new Set(filtered);
        }
    }
}
</script>


<style>

    .graph-section .slider {
        position: absolute;
        width: 100%;
        display: flex;
        padding: 0 1vw 0 1vw;
        flex-wrap: wrap;
        overflow-y: scroll;
        scroll-behavior: smooth;
        scroll-snap-type: x mandatory;

    }

    /* Hide scrollbar for Chrome, Safari and Opera */
    .graph-section .slider::-webkit-scrollbar {
        display: none;
    }

    /* Hide scrollbar for IE, Edge and Firefox */
    .graph-section .slider {
        -ms-overflow-style: none;  /* IE and Edge */
        scrollbar-width: none;  /* Firefox */
    }

    .graph-section .slider .graph{
        position: relative;
        width: 33%;
        height: 7.5vw;
        flex-shrink: 0;
        transform-origin: center center;
        transform: scale(1);
        scroll-snap-align: center;
        display: flex;
    }

    .graph-section .slider .graph:hover{
        background: rgba(217, 217, 217, 0.12);
    }

    .bookmark-graph {
        display: block;
        width: 0.9vw;
        height: 0.9vw;
        margin: 1% 1% 0 0;
        background-color: rgba(255, 255, 255, 0.62);
        -webkit-mask: url(@/assets/pathwaybar/star-solid.svg) no-repeat center;
        mask: url(@/assets/pathwaybar/star-solid.svg) no-repeat center;
        mask-size: 0.9vw;
        background-repeat: no-repeat;
    }

    .remove-graph {
        width: 0.9vw;
        height: 0.9vw;
        -webkit-filter: invert(100%); /* Safari/Chrome */
        filter: invert(100%);
        margin: 1% 1% 0 0;
    }

    .graph-options {
        position: fixed;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: end;
    }

    .graph-name {
        position: fixed;
        display: flex;
        bottom: 5%;
        width: 100%;
        height: 20%;
        -webkit-backdrop-filter: blur(7.5px);
        text-align-last: center;
        justify-content: center;
    }

    .graph-name input[type=text] {
        font-size: 0.85vw;
        background: none;
        color: white;
        cursor: default;
        font-family: 'ABeeZee', sans-serif;
        border: none;
    }

    .checked {
        background-color: #ffa500;
    }

    .slider span {
        width: 100%;
        height: 100%;
        text-align: center;
        color: white;
        font-size: 0.7vw;
    }

</style>