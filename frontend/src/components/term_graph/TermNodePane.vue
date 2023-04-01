<template>
    <div class="text" v-if="active_node !== null">
        <div class="headertext">
            <span>{{active_node.attributes['Name']}}</span>
        </div>
        <button v-on:click="to_proteins()" >To Protein Graph</button>
        <div class="nodeattributes">
            <div id="colorbar" :style="{ backgroundColor: colornode }">{{active_node.attributes['Modularity Class']}}</div>
            <div class="data">
                <span><i>{{active_node.attributes["Description"]}}</i></span><br/><br/>
            </div>
            <div class="p">
            <span>Statistics:</span>
            <button v-on:click="expand_proteins()" id="expand-btn">Expand</button>
            </div>
            <div class="p">
            <span>Connections:</span>
            <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
            <button v-on:click="expand_proteins()" id="expand-btn">Expand</button>
            </div>
            <div class="link" id="link">
                <ul>
                    <li class="membership" v-for="link in links" :key="link.id" >
                        <a href="#" v-on:click="select_node(link.id)">{{link.label}}</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'TermNodePane',
    props: ['active_node','term_data','node_color_index',],
    data() {
        return {
            links: null,
            colornode: null
        }
    },
    watch: {
        active_node() {
            var com = this;

            
            if (com.active_node == null) {
                return;
            }
            
            com.colornode = com.node_color_index[com.active_node.attributes["Ensembl ID"]]

            const neighbors = {};
            com.term_data.edges.forEach(e => {
                if (com.active_node.id == e.source) {
                    neighbors[e.target] = true;
                }
                if (com.active_node.id == e.target) {
                    neighbors[e.source] = true;
                }
            });

            com.links = com.term_data.nodes.filter(obj => neighbors[obj.id]);
            

        }
    },
    methods: {
        
        copyclipboard(){
            var com = this;

            var textToCopy = [];
            for(var link of com.links) textToCopy.push(link.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        expand_proteins() {
            
            const div = document.getElementById("link")

            if(div.style.visibility == "visible"){
                div.style.visibility = "hidden";
            }else{
                div.style.visibility = "visible";
            }
            
        },
        to_proteins(){
            var com = this;
            this.$store.commit('assign_active_enrichment', com.active_node.attributes["Ensembl ID"])
            this.$router.push("protein")
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