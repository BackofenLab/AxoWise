<template>
    <div class="slider" tabindex="0">
        <div v-for="(entry, index) in filt_graphs" :key="index" class="graph" v-on:click="switch_graph(entry)" @mouseover="activeGraphIndex = index" @mouseout="activeGraphIndex = -1">
            <SnapshotGraph :propValue="entry" :index="entry.id"/>
            <div class="graph-options" v-show="activeGraphIndex == index" >
                <div class="bookmark-graph" v-on:click.stop="add_graph(entry)" :class="{ checked: favourite_graphs.has(entry)}" ref="checkboxStatesGraph"></div>
                <img  class="remove-graph" src="@/assets/pathwaybar/cross.png" v-on:click.stop="remove_graph(entry)">
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
    props: ['gephi_data','filtered_terms', 'bookmark_off'],
    components: {
        SnapshotGraph,
    },
    data() {
        return {
            api: {
                termgraph: "api/subgraph/terms",
            },
            term_graphs: new Set(),
            favourite_graphs: new Set(),
            activeGraphIndex: -1,
            graph_number: 0,
        }
    },
    mounted(){
        this.emitter.on("generateGraph", (set) => {
            this.get_term_data(set)
        });
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
                        if(this.term_graphs.size < 1) this.$store.commit('assign_term_graph', response.data)
                        this.$store.commit('assign_new_term_graph', {label: `Graph ${this.graph_number}`, graph: response.data})
                        this.term_graphs.add({ id: this.graph_number, label: `Graph ${this.graph_number}`, graph: response.data});
                    }
                })

        },
        switch_graph(entry) {
            this.$store.commit('assign_term_graph', entry.graph)
            this.$router.push("terms")
        },
        remove_graph(entry) {
            if (!this.favourite_graphs.has(entry)) {
                // Checkbox is checked, add its state to the object
                this.favourite_graphs.delete(entry)
            }
            this.term_graphs.delete(entry)
            this.$store.commit('remove_snapshotPathway', entry.id)
        },
        add_graph(entry){
            if (!this.favourite_graphs.has(entry)) {
                // Checkbox is checked, add its state to the object
                this.favourite_graphs.add(entry)
            } else {
                // Checkbox is unchecked, remove its state from the object
                this.favourite_graphs.delete(entry)
            }
        },
    },
    computed: {
        filt_graphs() {
            var com = this;
            var filtered = [...com.term_graphs];

            if (!com.bookmark_off){
                filtered = filtered.filter(function(term) {
                    return com.favourite_graphs.has(term)
                });
            }

            return new Set(filtered);
        }
    }
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
        border-radius: 5px;
        z-index: 999;
        font-family: 'ABeeZee', sans-serif;
    }
    .generate-graph {
        width: 24.20%;
        height: 11.16%;
        position: absolute;
        border-radius: 5px;
        background: #0A0A1A;
        cursor: default;
    }
    .generate-graph .generate-text {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.95vw;
    }

    .graph-section {
        width: 100%;
        height: 87.65%;
        top: 12.35%;
        display: flex;
        border-radius: 5px;
        background: #0A0A1A;
        position: absolute;
        justify-content: center;
    }

    .graph-section .slider {
        position: absolute;
        width: 90.78%;
        height: 100%;
        display: flex;
        align-items: center;
        overflow-x: scroll;
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
        width: 31.4%;
        height: 71.71%;
        flex-shrink: 0;
        margin: 0% 1% 0% 1%;
        border-radius: 5px;
        border: 1px solid #FFF;
        background: rgba(217, 217, 217, 0.12);
        transform-origin: center center;
        transform: scale(1);
        scroll-snap-align: center;
        display: flex;
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
        border-radius: 0 0 5px 5px;
        background-color: #0A0A1A;
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

</style>