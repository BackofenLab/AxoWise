<template>
    <div id="de-connect" class="connect">
        <div class="selection-results">
            <table >
                <tbody>
                    <tr v-for="(key,entry, index) in selectionattr" :key="index" class="option">
                        <td>
                            <div class="statistics-attr">
                                <a href="#">{{entry}}</a>
                            </div>
                        </td>
                        <td>
                            <input class="statistics-val"
                            type="number"
                            v-bind:min="key.min"
                            v-bind:max="key.max"
                            v-bind:step="key.step"
                            v-model="key.value"
                            v-on:change="select_proteins()"
                            >
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="sorting">
            <a class="node_filter" v-on:click="sort_node = (sort_node === 'asc') ? 'dsc' : 'asc'; sort_cluster = ''; sort_degree = '' " >nodes</a>
            <a class="cluster_filter" v-on:click="sort_cluster = (sort_cluster === 'asc') ? 'dsc' : 'asc'; sort_node = ''; sort_degree = '' " >cluster</a>
            <a class="degree_filter" v-on:click="sort_degree = (sort_degree === 'asc') ? 'dsc' : 'asc'; sort_cluster = ''; sort_node = '' " >degree</a>
        </div>

        <div class="network-results" tabindex="0" @keydown="handleKeyDown">
            <table >
                <tbody>
                    <tr v-for="(entry, index) in filt_links" :key="index" class="option">
                        <td>
                            <div class="statistics-attr">
                                <a href="#">{{entry.attributes["Name"]}}</a>
                            </div>
                        </td>
                        <td>
                            <a class="statistics-val">{{entry.attributes["Modularity Class"]}}</a>
                        </td>
                        <td>
                            <a class="statistics-val">{{entry.attributes["Degree"]}}</a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

export default {
    name: 'RegulatedProteins',
    props: ['active_decoloumn','gephi_data'],
    data() {
        return {
            dvalueNodes: [],
            minSelect: {
                value: -10,
                min: -10,
                max: 0,
                step: 0.1            
            },
            maxSelect: {
                value: 10,
                min: 0,
                max: 10,
                step: 0.1
            },
            selectionattr:{},
            sort_node: "",
            sort_cluster: "",
            sort_degree: "",
        }
    },
    watch: {
        active_decoloumn(){
            var com = this

            com.dvalueNodes = this.gephi_data.nodes
            var dvalue_list = Object.values(com.gephi_data.nodes).map(item => item.attributes[com.active_decoloumn]).filter(value => value !== undefined)
            com.maxSelect.value = Math.max(...dvalue_list)
            com.minSelect.value = Math.min(...dvalue_list)
            com.selectionattr = {max: com.maxSelect, min: com.minSelect}

        }
    },
    methods: {
        select_proteins() {
            this.dvalueNodes = []
            for (var node of this.gephi_data.nodes) {
                var dvalue = node.attributes[this.active_decoloumn]
                if (dvalue >= this.minSelect.value && dvalue <= this.maxSelect.value) this.dvalueNodes.push(node);
            }

            this.emitter.emit("selectDE", this.dvalueNodes);

            },
    },
    computed: {
        filt_links() {
            var com = this;
            var filtered = com.dvalueNodes;

            if(com.sort_node == "asc"){
                filtered.sort(function(t1, t2) { 
                    return (t1.attributes["Name"].toLowerCase() > t2.attributes["Name"].toLowerCase() 
                    ? 1 : (t1.attributes["Name"].toLowerCase() === t2.attributes["Name"].toLowerCase() ? 0 : -1)) })
            }else if(com.sort_node == "dsc"){
                filtered.sort(function(t1, t2) { 
                    return (t2.attributes["Name"].toLowerCase() > t1.attributes["Name"].toLowerCase() 
                    ? 1 : (t1.attributes["Name"].toLowerCase() === t2.attributes["Name"].toLowerCase() ? 0 : -1)) })
            }

            if(com.sort_cluster == "asc"){
                filtered.sort((t1, t2) => t2.attributes["Modularity Class"] - t1.attributes["Modularity Class"])
            }else if (com.sort_cluster == "dsc"){
                filtered.sort((t1, t2) => t1.attributes["Modularity Class"] - t2.attributes["Modularity Class"])
            }

            if(com.sort_degree == "asc"){
                filtered.sort((t1, t2) => t2.attributes["Degree"] - t1.attributes["Degree"] )
            }else if (com.sort_degree == "dsc"){
                filtered.sort((t1, t2) => t1.attributes["Degree"]  - t2.attributes["Degree"] )
            }

            return new Set(filtered);
        },
    }
}
</script>

<style>

#de-connect {
    width: 100%;
    height: 100%;
    font-family: 'ABeeZee', sans-serif;
    padding: 1.3vw 1.3vw 1vw 1.3vw;
    overflow: scroll;
}

.selection-results input[type=number] { 
    border: none;
    font-family: 'ABeeZee', sans-serif;
    font-size: 0.7vw;
    color: white;
    background: none;
    -moz-appearance: textfield;
    -webkit-appearance: textfield;
    appearance: textfield;
    text-align: left;
}

.selection-results::-webkit-scrollbar,
#de-connect::-webkit-scrollbar {
  display: none;
}

.selection-results table {
    display: flex;
    width: 100%;
}

:focus {outline:0 !important;}

.selection-results table tbody{
    width: 100%;
}
.selection-results td:first-child {
    width: 70%;
    align-self: center;
}
.selection-results td:last-child {
    font-size: 0.7vw;
    margin-bottom: 1%;
    color: white;
    width:  30%;
    align-self: center;
    white-space: nowrap;
    overflow: hidden;    /* Hide overflow content */
    text-overflow: ellipsis;
}
</style>