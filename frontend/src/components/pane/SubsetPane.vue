<template>
    <div class="text" v-if="active_subset !== null">
        <div class="headertext">
            <span>Subset</span>
        </div>
        <button id="hide-btn" class="subset-btn" v-on:click="show_layer()">Hide</button>
        <div class="change-level-menu">
            <button id="apply-func-btn" class="subset-btn" v-on:click="apply_func(true)">Apply</button>
            <button id="revert-func-btn" class="subset-btn" v-on:click="apply_func(false)">Revert</button>
        </div>
        <div class="data">
                <span><strong>Number of Proteins: </strong>{{number_prot}}</span><br/><br/>
                <span><strong>Number of Links: </strong>{{number_asc}}</span><br/><br/>
        </div>
        <div class="nodeattributes">
            <div class="p">
                <span>Connections:</span>
                <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
                <button v-on:click="expand_proteins=!expand_proteins" id="expand-btn">Expand</button>
            </div>
            <div class="link" id="link" v-show="expand_proteins === true">
                <ul>
                    <li class="membership" v-for="link in active_subset" :key="link" >
                        <a href="#" v-on:click="select_node(link)">{{link.label}}</a>
                    </li>
                </ul>
            </div>
            <div class="p2">
                <b>Links:</b>
                <button v-on:click="expand_links=!expand_links" id="expand-btn">Expand</button>
                </div>
                    <div class="link" id="edges" v-show="expand_links === true">
                        <ul>
                            <li v-for="edge in contained_edges" :key="edge">
                                <div class="edge">
                                <a href="#" v-on:click="select_node(edge.source[0])">{{edge.source[1]}}</a>
                                <a href="#" v-on:click="select_node(edge.target[0])">{{edge.target[1]}}</a>
                                </div>
                            </li>
                        </ul>
                    </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'SubsetPane',
    props: ['active_subset','gephi_data'],
    emits: ['active_item_changed', 'highlight_subset_changed'],
    data() {
        return {
            hide: true,
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

            com.$emit('active_item_changed',{ "subset": com.subset_item })
            
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
                this.emitter.emit("hideSubset", null);
            }
            com.hide = !com.hide
        },

        /**
        * Calling the procedure in component EnrichmentTool for enriching terms with given set.
        * @param {boolean} state - functional enrichment gets reverted or applied.
        */
        apply_func(state) {
            if (state) this.emitter.emit("enrichSubset", this.active_subset.map(node => node.attributes["Name"]));
            else this.emitter.emit("enrichSubset", null);
        },

        /**
        * Calling the procedure in component MainVis to highlight a specific node
        * @param {dict} value - A dictionary of a single node
        */
        select_node(value) {
            this.emitter.emit("searchNode", value);
        }
    },
}
</script>

<style>
    #subsetpane {
        visibility: hidden;
    }
    .pane-show {
        transform: translateX(326px);
    }

    .subset-btn {
        position: relative;
        color: #fff;
        border-style: outset;
        border-width: 1px;
        border-radius: 20px;
        padding: 3px;
        background-color: rgba(0, 0, 0, 0.7);
        margin-bottom: 5px;
        justify-content: center;
    }

</style>
