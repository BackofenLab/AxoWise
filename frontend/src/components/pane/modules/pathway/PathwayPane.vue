<template>
    <div class="text" v-show="active_node !== null">
        <div id="colorbar-pathway">
            <div class='colorbar-text' :style="{ backgroundColor: colornode }" v-if="active_node !== null">
                {{active_node.attributes["Name"]}}
            </div>
            <div class='colorbar-img colortype' v-on:click="to_proteins()">
                <img src="@/assets/pane/follow.png">
            </div>
        </div>
        <div class="nodeattributes">
            <div id="informations" class="subsection">
                <div class="subsection-header">
                    <span>informations</span>
                </div>
                <div class="subsection-main colortype">
                </div>
            </div>
            <div id="network" class="subsection">
                <div class="subsection-header">
                    <span>network statistics</span>
                </div>
                <div class="subsection-main colortype">
                    <NetworkStatistics
                    :active_node='active_node' 
                    ></NetworkStatistics>
                </div>
            </div>
            <div id="connections" class="subsection">
                <div class="subsection-header">
                    <span>connections</span>
                </div>
                <div class="subsection-main colortype">
                    <NodeConnections
                    :active_node='active_node'
                    :links='links'
                    ></NodeConnections>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import NetworkStatistics from '@/components/pane/modules/node/NetworkStatistics.vue'
import NodeConnections from '@/components/pane/modules/node/NodeConnections.vue'

export default {
    name: 'PathwayPane',
    props: ['active_node','gephi_data','node_color_index','mode'],
    emits: ['active_item_changed'],
    components: {
        NetworkStatistics,
        NodeConnections,

    },
    data() {
        return {
            links: null,
            colornode: null,
            node_item: {
                value: null,
                imageSrc: require('@/assets/pane/protein-icon.png')
            },
            nodes: this.gephi_data.nodes,
        }
    },
    watch: {
        active_node() {
            var com = this;
            
            if (com.active_node == null) {
                return;
            }

            com.node_item.value = com.active_node
            
            com.$emit('active_item_changed',{ "Protein": com.node_item})
            
            com.colornode = com.node_color_index[com.active_node.attributes["Ensembl ID"]]


            const neighbors = {};
            const node_id = com.active_node.attributes["Ensembl ID"]
            com.gephi_data.edges.forEach(e => {
                if (node_id == e.source) {
                    neighbors[e.target] = true;
                }
                if (node_id == e.target) {
                    neighbors[e.source] = true;
                }
            });

            com.links = com.gephi_data.nodes.filter(obj => neighbors[obj.id]);

        }
    },
    methods: {
        copyclipboard(){
            var com = this;

            var textToCopy = [];
            for(var link of com.links) textToCopy.push(link.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        select_node(value) {
            this.emitter.emit("searchNode", {node: value, mode: this.mode});
        },
        to_proteins(){
            var com = this;
            this.$store.commit('assign_active_enrichment', com.active_node.attributes["Ensembl ID"])
            this.$router.push("protein")
        }
        
    },
}
</script>

<style>
</style>