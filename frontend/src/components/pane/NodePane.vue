<template>
    <div class="text" v-if="active_node !== null">
        <div class="headertext">
            <span>{{active_node.attributes['Name']}}</span>
        </div>
        <div class="nodeattributes">
            <div id="colorbar" :style="{ backgroundColor: colornode }">{{active_node.attributes['Modularity Class']}}</div>
            <div class="data">
                <span><i>{{active_node.attributes["Description"]}}</i></span><br/><br/>
            </div>
            <div class="p">
            <span>Statistics:</span>
            <button v-on:click="expand_stats = !expand_stats" id="expand-btn">Expand</button>
            </div>
            <div class="statistics" id="statistics" v-show="expand_stats === true">
                <ul>
                    <li class="membership" v-for="(value, key) in statistics" :key="key" >
                        <span><strong>{{key}}: </strong>{{value}}</span>
                    </li>
                </ul>
            </div>
            <div class="p">
            <span>Connections:</span>
            <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
            <button v-on:click="expand_neighbor = !expand_neighbor" id="expand-btn">Expand</button>
            </div>
            <div class="link" id="link" v-show="expand_neighbor === true">
                <ul>
                    <li class="membership" v-for="link in links" :key="link" >
                        <a href="#" v-on:click="select_node(link)">{{link.label}}</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'NodePane',
    props: ['active_node','gephi_data','node_color_index',],
    emits: ['active_item_changed'],
    data() {
        return {
            links: null,
            colornode: null,
            statistics: {},
            expand_neighbor: false,
            expand_stats: false,
            node_item: {
                value: null,
                imageSrc: require('@/assets/pane/protein-icon.png')
            }
        }
    },
    watch: {
        active_node() {
            var com = this;
            
            if (com.active_node == null) {
                return;
            }

            com.node_item.value = com.active_node
            
            com.$emit('active_item_changed',{ "node": com.node_item})
            
            com.colornode = com.node_color_index[com.active_node.attributes["Ensembl ID"]]
            const { Degree, "Ensembl ID": EnsemblID } = com.active_node.attributes;
            com.statistics = { Degree, EnsemblID }
            if(com.$store.state.dcoloumns != null) {
                com.$store.state.dcoloumns.forEach(dcoloumn => {
                    com.statistics[dcoloumn] = com.active_node.attributes[dcoloumn]
                });
            }


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
        }
    }
}
</script>

<style>

    .pane-show {
        transform: translateX(326px);
    }
    #colorbar {
        display: block;
        border-radius: 20px;
        width: 50%;
        height: 20px;
        color: white;
        text-align: center;
        transform: translate(50%);
    }

</style>