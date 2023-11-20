<template>
    <div class="text" v-show="active_node !== null">
        <div id="colorbar-pathway">
            <div class='colorbar-text' :style="{ backgroundColor: colornode }" v-if="active_node !== null">
                {{active_node.attributes["Name"]}}
            </div>
            <div class='colorbar-img' v-on:click="to_proteins()">
                <img src="@/assets/pane/follow.png">
            </div>
        </div>
        <div class="nodeattributes">
            <div id="informations" class="subsection">
                <div class="subsection-header">
                    <span>informations</span>
                </div>
                <div class="subsection-main">
                </div>
            </div>
            <div id="network" class="subsection">
                <div class="subsection-header">
                    <span>network statistics</span>
                </div>
                <div class="subsection-main">
                    <NetworkStatistics
                    :active_node='active_node' 
                    ></NetworkStatistics>
                </div>
            </div>
            <div id="connections" class="subsection">
                <div class="subsection-header">
                    <span>connections</span>
                </div>
                <div class="subsection-main">
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

    .pane-show {
        transform: translateX(326px);
    }
    #colorbar {
        position: relative;
        display: flex;
        border-radius: 5px;
        margin-top: 5%;
        width: 50%;
        color: white;
        align-items: center;
        justify-content: center;
        transform: translate(50%);
        font-family: 'ABeeZee', sans-serif;
        font-size: 0.9vw;
    }
    .nodeattributes{
        position: absolute;
        display: flex;
        flex-direction: column;
        width: 100%;
        height: 100%;
        margin-top: 10%;
        align-items: center;
    }
    .nodeattributes .subsection {
        margin-bottom: 4%;
        position: relative;
        width: 90%;
    }

    .subsection .subsection-header {
        position: absolute;
        height: 1vw;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.4);
        border-radius: 5px 5px 0 0;
        display: flex;
        justify-content: left;
        align-items: center;
        font-family: 'ABeeZee', sans-serif;
        font-size: 0.7vw;
        padding-left: 3%;
        z-index: 999;
    }

    .subsection .subsection-main {
        position: absolute;
        height: 100%;
        width: 100%;
        background: #0A0A1A;
        border-radius: 5px;
    }

    #informations {
        height: 25.78%;
    }

    #routing {
        height: 20%;
    }

    #network {
        height: 16%;
    }

    #connections {
        height: 18%;
    }


</style>