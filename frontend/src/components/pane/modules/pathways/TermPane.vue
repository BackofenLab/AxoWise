<template>
    <div class="text" v-show="active_term !== null">
        <div id="colorbar-pathway">
            <div class='colorbar-text' v-if="active_term !== null">
                {{active_term.name}}
            </div>
            <div class='colorbar-img' v-on:click="to_term()">
                <img src="@/assets/pane/follow.png">
            </div>
        </div>
        <div class="nodeattributes">
            <div id="network" class="subsection">
                <div class="subsection-header">
                    <span>pathway statistics</span>
                </div>
                <div class="subsection-main">
                    <PathwayStatistics
                    :active_term='active_term' 
                    ></PathwayStatistics>
                </div>
            </div>
            <div id="pathway-connections" class="subsection">
                <div class="subsection-header">
                    <span>connections</span>
                </div>
                <div class="subsection-main">
                    <PathwayConnections
                    :active_term='active_term'
                    :gephi_data='gephi_data'
                    ></PathwayConnections>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import PathwayStatistics from '@/components/pane/modules/pathways/PathwayStatistics.vue'
import PathwayConnections from '@/components/pane/modules/pathways/PathwayConnections.vue'

export default {
    name: 'TermPane',
    props: ['active_term','gephi_data','mode'],
    emits: ['active_item_changed', 'highlight_subset_changed'],
    components:{
        PathwayStatistics,
        PathwayConnections
    },
    data() {
        return {
            term_history: [],
            expand_stats: false,
            expand_proteins: false,
            term_item: {
                value: null,
                imageSrc: require('@/assets/pane/enrichment-icon.png')
            }
        }
    },
    watch: {
        active_term() {
            var com = this
            if (com.active_term == null) {
                return;
            }

            com.term_item.value = com.active_term
            com.$emit('active_item_changed',{ "Pathway": com.term_item })

        }
    },
    methods: {
        copyclipboard(){
            var com = this;

            var textToCopy = [];
            for(var link of com.links) textToCopy.push(link.label); 
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        to_term(){
            var com = this;
            if(!com.$store.state.term_graph_data) {
                alert("There is no term graph")
                return
            }

            this.$store.commit('assign_active_enrichment_node', com.active_term)
            this.$router.push("terms")
        },
        select_node(value) {
            this.emitter.emit("searchNode", {node: value, mode: this.mode});
        },
    }
}
</script>

<style>
    #colorbar-pathway{
        position: relative;
        display: flex;
        border-radius: 5px;
        margin-top: 5%;
        width: 70%;
        color: white;
        align-items: center;
        text-align: center;
        justify-content: center;
        transform: translate(13.5%);
        font-family: 'ABeeZee', sans-serif;
        font-size: 0.9vw;
    }
    .colorbar-text {
        width: 100%;
        background-color: darkgreen;
        border-radius: 5px 0 0 5px;
    }
    .colorbar-img {
        width: 15%;
        left: 100%;
        height: 100%;
        position: fixed;
        display: -webkit-flex;
        align-items: center;
        background-color: #0A0A1A;
        padding: 1%;
        border-radius: 0 5px 5px 0;
    }

    .colorbar-img img {
        padding: 5% 23% 5% 23%;
        filter: invert(100%);
    }

    #pathway-connections {
        height: 40%;
    }

</style>