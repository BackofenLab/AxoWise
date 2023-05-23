<template>
    <div class="graphselection">
        <v-select v-model="selected_graph" :options="graphs"  @update:model-value="retrieve_graph()"></v-select>
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
        }
    }
})
</script>

<style>
    .graphselection {
        position: absolute;
        display: block;
        width: 200px;
        top: 10px;
        right: 0;
    }
</style>
