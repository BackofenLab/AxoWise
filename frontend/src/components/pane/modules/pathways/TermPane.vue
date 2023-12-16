<template>
    <div class="text" v-show="active_term !== null">
        <div id="colorbar-pathway">
            <div class="favourite-pane-symbol">
                <label class="custom-checkbox">
                    <div class="checkbox-image" v-if="favourite_pathways != null" v-on:click="bookmark_pathway()" :class="{ checked: favourite_pathways.has(active_term)}" ></div>
                </label>
            </div>
            <div class='colorbar-text' v-if="active_term !== null">
                {{active_term.name}}
            </div>
            <div class='colorbar-img colortype' v-on:click="to_term()">
                <img src="@/assets/pane/follow.png">
            </div>
        </div>
        <div class="nodeattributes">
            <div id="network" class="subsection">
                <div class="subsection-header">
                    <span>pathway statistics</span>
                </div>
                <div class="subsection-main colortype">
                    <PathwayStatistics
                    :active_term='active_term' 
                    ></PathwayStatistics>
                </div>
            </div>
            <div id="pathway-connections" class="subsection">
                <div class="subsection-header">
                    <span>connections</span>
                    <img src="@/assets/pane/copy.png" v-on:click="copyclipboard()">
                </div>
                <div class="subsection-main colortype">
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
            },
            favourite_pathways: this.$store.state.favourite_enrichments
        }
    },
    watch: {
        active_term() {
            var com = this
            if (com.active_term == null) {
                return;
            }


            this.favourite_pathways = this.$store.state.favourite_enrichments

            console.log(this.favourite_pathways)

            com.term_item.value = com.active_term
            com.$emit('active_item_changed',{ "Pathway": com.term_item })

        }
    },
    methods: {
        copyclipboard(){
            this.emitter.emit("copyConnections");
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
        bookmark_pathway(){
            this.emitter.emit("bookmarkPathway", this.active_term);
            this.favourite_pathways = this.$store.state.favourite_enrichments
        }
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
        background-color: darkgreen;
        border-radius: 5px 0 0 5px;
    }
    .colorbar-text {
        width: 100%;
        background-color: darkgreen;
        padding: 2%;
        border-radius: 5px 0 0 5px;
    }
    .colorbar-img {
        width: 15%;
        left: 100%;
        height: 100%;
        position: fixed;
        display: -webkit-flex;
        align-items: center;
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

    .favourite-pane-symbol{
        height: 100%;
        width: 10%;
        left: 2%;
        justify-content: center;
        text-align: center;
        position: relative;
        display: flex;
        
    }
    .favourite-pane-symbol .custom-checkbox {
        position: relative;
        display: inline-block;
        cursor: default;
    }

    .checked {
        background-color: #ffa500;
    }

</style>