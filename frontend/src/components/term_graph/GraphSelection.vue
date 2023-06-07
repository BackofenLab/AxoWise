<template>
    <div class="graphselection">
        <button id="remove-graph-btn" v-on:click="remove_graph()">-</button>
        <v-select id="select-graph" v-model="selected_graph" :options="graphs" :clearable="false" :model-value="selected_graph" @update:model-value="retrieve_graph()"></v-select>
    </div>
</template>

<script>
export default ({
    name: 'GraphSelection',
    props:['term_data'],
    emits:['term_data_changed'],
    data() {
        return {
            selected_graph: null,
            graphs: this.$store.state.term_graph_dict

        }
    },
    watch:{
        term_data(){
            this.graphs = this.$store.state.term_graph_dict
        }
    },
    methods: {
        retrieve_graph(){
            this.$store.commit('assign_term_graph', this.selected_graph.graph)
            this.$emit('term_data_changed', this.selected_graph.graph)
        },
        remove_graph() {

            
            for (var k in this.graphs){
                if(this.selected_graph == this.graphs[k]) {
                    if(k != 0){
                        this.selected_graph = this.graphs[0]
                        this.graphs.splice(k,1);
                        this.$emit('term_data_changed', this.graphs[0].graph)
                    }
                }
            }
        }
    }
})
</script>

<style>
    #select-graph {
        width: 100%;
        margin-left: 5px;
    }

    #remove-graph-btn {

        width: 20px;
        height: 20px;
        border-radius: 100%;
        border-style: none;
        margin-left: 10px;
        z-index: 999;
        position: absolute;
        background-color: rgba(0,0,0,0.2);
    }

    .graphselection {
        position: absolute;
        display: flex;
        width: 200px;
        top: 10px;
        right: 0;
        align-items: center;
    }
</style>
