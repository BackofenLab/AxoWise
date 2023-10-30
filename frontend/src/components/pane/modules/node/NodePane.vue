<template>
    <div class="text" v-show="active_node !== null">
        <div id="colorbar" v-if="active_node !== null" :style="{ backgroundColor: colornode }">{{active_node.attributes['Name']}}</div>
        <div class="nodeattributes">
            <div id="informations" class="subsection">
                <div class="subsection-header">
                    <span>informations</span>
                </div>
                <div class="subsection-main">
                    <ChatbotInformation
                    :active_node='active_node'
                    ></ChatbotInformation>
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
            <div id="routing" class="subsection">
                <div class="subsection-header">
                    <span>routing</span>
                </div>
                <div class="subsection-main">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import NetworkStatistics from '@/components/pane/modules/node/NetworkStatistics.vue'
import NodeConnections from '@/components/pane/modules/node/NodeConnections.vue'
import ChatbotInformation from '@/components/pane/modules/node/ChatbotInformation.vue'

export default {
    name: 'NodePane',
    props: ['active_node','gephi_data','node_color_index',],
    emits: ['active_item_changed'],
    components: {
        NetworkStatistics,
        ChatbotInformation,
        NodeConnections

    },
    data() {
        return {
            links: null,
            colornode: null,
            expand_neighbor: false,
            expand_stats: false,
            node_item: {
                value: null,
                imageSrc: require('@/assets/pane/protein-icon.png')
            },
            nodes: this.gephi_data.nodes,
            selected_protein: null,
            path: true,
            protein_name:""
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
            this.emitter.emit("searchNode", value);
        },
        retrieve_path() {
            this.path = true
            if(this.selected_protein == null) {
                this.emitter.emit("reset_protein", this.active_node)
                return
            }
            this.emitter.emit("searchPathway", {"source":this.active_node.id ,"target": this.selected_protein.id});
        },
        
    },
    mounted(){
        this.emitter.on("emptySet", (state) => {
            this.path = state
        });

    }
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
        height: 18%;
    }

    #network {
        height: 16%;
    }

    #connections {
        height: 18%;
    }


</style>