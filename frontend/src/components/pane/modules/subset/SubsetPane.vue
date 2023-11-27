<template>
    <div class="text" v-show="active_subset !== null">
        <div id="colorbar-subset">
            <div class='colorbar-text' v-if="active_subset !== null">
               No° nodes: {{number_prot}}
            </div>
            <div class='colorbar-img colortype' v-on:click="show_layer()">
                <img src="@/assets/pane/invisible.png" v-if="!hide">
                <img src="@/assets/pane/visible.png" v-if="hide">
            </div>
        </div>
        <div class="nodeattributes">
            <div id="subset-connections" class="subsection">
                <div class="subsection-header">
                    <span>contained proteins</span>
                </div>
                <div class="subsection-main colortype">
                    <SubsetConnections
                    :active_subset='active_subset' 
                    ></SubsetConnections>
                </div>
            </div>
            <div id="network" class="subsection">
                <div class="subsection-header">
                    <span>contained edges ({{number_asc}})</span>
                </div>
                <div class="subsection-main colortype">
                    <SubsetLinks
                    :contained_edges='contained_edges' 
                    ></SubsetLinks>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import SubsetConnections from '@/components/pane/modules/subset/SubsetConnections.vue'
import SubsetLinks from '@/components/pane/modules/subset/SubsetLinks.vue'

export default {
    name: 'SubsetPane',
    props: ['active_subset','gephi_data', 'mode'],
    emits: ['active_item_changed', 'highlight_subset_changed'],
    components: {
        SubsetConnections,
        SubsetLinks
    },
    data() {
        return {
            hide: false,
            expand_proteins: false,
            subset_item: {
                value: null,
                imageSrc: require('@/assets/pane/cluster-icon.png')
            },
            number_prot: "",
            number_asc: "",
            contained_edges: [],
            export_edges: [],
            subset_ids: [],
            expand_links: false


        }
    },
    watch: {
        active_subset() {
            var com = this;
            
            if (com.active_subset == null) {
                return;
            }

            com.subset_item.value = com.active_subset

            com.contained_edges = [];
            com.export_edges = [];
            com.subset_ids = [];

            var id_dict = {};
            for (var idX in com.active_subset){
                id_dict[com.active_subset[idX].id] = com.active_subset[idX].label;
                com.subset_ids.push(com.active_subset[idX].id);
            }
            var subset_proteins = new Set(com.subset_ids);
            for (var idx in com.gephi_data.edges) {
                var edge = com.gephi_data.edges[idx];
                if(subset_proteins.has(edge.source) && subset_proteins.has(edge.target)){
                    if(edge.source != null && edge.target != null){
                        com.export_edges.push(edge);
                        com.contained_edges.push({
                            
                            "source": [edge.source, id_dict[edge.source]],
                            "target": [edge.target, id_dict[edge.target]]
                        
                        });
                    }
                }
            }

            com.number_asc = com.export_edges.length.toString()
            com.number_prot = com.subset_ids.length.toString()

            com.$emit('active_item_changed',{ "Subset": com.subset_item })
            
        }
    },
    methods: {
        copyclipboard(){
            var com = this;

            var textToCopy = [];
            for(var link of com.active_subset) textToCopy.push(link.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        show_layer(){
            var com = this;

            if(com.hide){
                this.emitter.emit("hideSubset", com.active_subset.map(node => node.attributes["Name"]));
            }
            else{
                this.emitter.emit("hideSubset", {subset: null, mode: this.mode});
            }
            com.hide = !com.hide
        },

        /**
        * Calling the procedure in component MainVis to highlight a specific node
        * @param {dict} value - A dictionary of a single node
        */
        select_node(value) {
            this.emitter.emit("searchNode", {node: value, mode: this.mode});
        }
    },
}
</script>

<style>
    #colorbar-subset{
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
    #colorbar-subset .colorbar-text{
        background-color: rgb(0,100,100);
    }

    #subset-connections {
        height: 40%;
    }
</style>
