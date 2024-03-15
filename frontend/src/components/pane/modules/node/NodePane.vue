<template>
    <div class="text" v-show="active_node !== null">
        <div class="gene_attribute" v-if="active_node !== null">
            <div id="colorbar" :style="{ backgroundColor: colornode }"></div>
            <div class="gene" >{{active_node.attributes['Name']}};</div>
            <div class="gene_attr" > deg:{{active_node.attributes['Degree']}};</div>
            <div class="gene_attr" > pr:{{Math.abs(Math.log10(active_node.attributes["PageRank"])).toFixed(2)}}</div>
        </div>
        <div :class="{'tool-section': !tool_active, 'tool-section-active': tool_active }">
            <div id="informations" class="subsection" v-show="tool_active && active_section == 'information'">
                <div class="subsection-header">
                    <span>informations</span>
                </div>
                <div class="subsection-main colortype">
                    <ChatbotInformation
                    :active_node='active_node'
                    ></ChatbotInformation>
                </div>
            </div>
            <div id="network" class="subsection" v-show="tool_active && active_section == 'statistics'">
                <div class="subsection-header">
                    <span>network statistics</span>
                </div>
                <div class="subsection-main colortype">
                    <NetworkStatistics
                    :active_node='active_node' 
                    :mode='mode' 
                    ></NetworkStatistics>
                </div>
            </div>
            <div id="connections" class="subsection" v-show="tool_active && active_section == 'connections'">
                <div class="subsection-header">
                    <span>connections</span>
                    <img src="@/assets/pane/copy.png" v-on:click="copyclipboard()">
                </div>
                <div class="subsection-main colortype">
                    <NodeConnections
                    :active_node='active_node'
                    :links='links'
                    ></NodeConnections>
                </div>
            </div>
            <div id="routing" class="subsection" v-show="tool_active && active_section == 'routing'">
                <div class="subsection-header">
                    <span>routing</span>
                </div>
                <div class="subsection-main colortype">
                    <RoutingNode 
                    :active_node='active_node'
                    :gephi_data='gephi_data'
                    ></RoutingNode>
                </div>
            </div>
        </div>
        <div class="nodeattributes">
            <img  class="icons" src="@/assets/toolbar/menu-burger.png" v-on:click="change_section( 'information')">
            <img  class="icons" src="@/assets/toolbar/settings-sliders.png" v-on:click="change_section('statistics')">
            <img  class="icons" src="@/assets/toolbar/proteinselect.png" v-on:click="change_section('connections')">
            <img  class="icons" src="@/assets/toolbar/logout.png" v-on:click="change_section('routing')">

        </div>
    </div>
</template>

<script>
import NetworkStatistics from '@/components/pane/modules/node/NetworkStatistics.vue'
import NodeConnections from '@/components/pane/modules/node/NodeConnections.vue'
import ChatbotInformation from '@/components/pane/modules/node/ChatbotInformation.vue'
import RoutingNode from '@/components/pane/modules/node/RoutingNode.vue'

export default {
    name: 'NodePane',
    props: ['active_node','gephi_data','node_color_index','mode','tool_active'],
    emits: ['active_item_changed','tool_active_changed'],
    components: {
        NetworkStatistics,
        ChatbotInformation,
        NodeConnections,
        RoutingNode

    },
    data() {
        return {
            active: true,
            active_section: '',
            links: null,
            colornode: null,
            expand_neighbor: false,
            expand_stats: false,
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
        change_section(val){
            var com = this;

            if(com.tool_active && com.active_section == val) {
                com.active_section = ''
                com.$emit('tool_active_changed', false)
            }else
            {
                if(!com.tool_active) {
                    com.active_section = val
                    com.$emit('tool_active_changed',true)
                }
                
                if(com.tool_active && com.active_section != val) {
                    com.active_section = val
                    com.$emit('tool_active_changed', true)
                }
            } 
        },
        copyclipboard(){
            var com = this;

            var textToCopy = [];
            for(var link of com.links) textToCopy.push(link.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        select_node(value) {
            this.emitter.emit("searchNode", {node: value, mode: this.mode});
        },
        
    },
}
</script>

<style>

    .text {
        height: 100%;
    }

    .gene_attribute{
        display: flex;
        font-family: 'ABeeZee', sans-serif;
        align-items: center;
        color:  #0A0A1A;
        padding: 0 0.5vw 0 0.5vw;
    }
    .tool-section{
        height: 0vw;
    }

    .tool-section-active{
        height: 10vw;
    }

    #colorbar {
        position: relative;
        display: flex;
        border-radius: 100%;
        width: 0.5vw;
        height: 0.5vw;
    }
    .gene{
        margin-left: 0.3vw;
        font-size: 0.9vw;
    }
    .gene_attr{
        font-size: 0.8vw;
        margin-left: 0.3vw;
    }

    .nodeattributes{
        position: absolute;
        display: flex;
        width: 100%;
        height: 2vw;
        align-items: center;
        justify-content: center;
    }
    .nodeattributes .icons{
    width: 0.8vw;
    height: 0.8vw;
    margin: 0 0.5vw 0 0.5vw;
    }
    .nodeattributes .subsection {
        margin-bottom: 4%;
        position: relative;
        width: 90%;
    }

    .subsection .subsection-header {
        position: absolute;
        width: 100%;
        display: flex;
        justify-content: left;
        align-items: center;
        font-family: 'ABeeZee', sans-serif;
        font-size: 0.7vw;
        padding: 0.2vw 0 0 0.5vw;
        color: rgba(255,255,255,0.5);
        z-index: 999;
        background-color: #0A0A1A;
    }

    .subsection .subsection-header img{
        position: absolute;
        width: 50%;
        right: -15%;
        display: -webkit-flex;
        padding: 1%;
        padding: 5% 23% 5% 23%;
        filter: invert(100%);

    }

    .subsection .subsection-main {
        height: 100%;
        width: 100%;
    }

    #informations,
    #routing,
    #network,
    #connections {
        height: 100%;
    }


</style>