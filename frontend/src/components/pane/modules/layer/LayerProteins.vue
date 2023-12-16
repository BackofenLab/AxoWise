<template>
    <div id="layer-connect">
        <div class="pane-sorting">
            <a class="pane_attributes" >node</a>
            <a class="pane_values">cluster</a>
        </div>

        <div class="network-results" tabindex="0" @keydown="handleKeyDown">
            <table >
                <tbody>
                    <tr v-for="entry in intersectionSet" :key="entry" class="option">
                        <td>
                            <div class="statistics-attr">
                                <a href="#">{{entry.attributes["Name"]}}</a>
                            </div>
                        </td>
                        <td>
                            <a class="statistics-val">{{entry.attributes["Modularity Class"]}}</a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

export default {
    name: 'LayerProteins',
    props: ['active_termlayers','gephi_data', 'hiding_terms'],
    data() {
        return {
            intersectionSet: null,
        }
    },
    watch: {
        active_termlayers: {
            handler(newList) {
            var com = this

            if (newList == null) {
                return;
            }

            com.intersectionSet = new Set();
            var intersectionSet = new Set();

            for (var checkElement of com.active_termlayers.main){
                if(!com.hiding_terms.has(checkElement) && com.active_termlayers.main.size >= 1){
                    intersectionSet= new Set(checkElement.symbols);
                    break
                }

            }
                
            for (var element of com.active_termlayers.main){
                if(!com.hiding_terms.has(element)){
                    intersectionSet = new Set(element.symbols.filter((value) => intersectionSet.has(value)));
                }

            }

            for (var proteins of this.gephi_data.nodes){
                if(intersectionSet.has(proteins.attributes["Name"])){
                    com.intersectionSet.add(proteins)
                }
            }
            },
            deep:true,
        },
    },
    methods: {
        select_node(value) {
            this.emitter.emit("searchNode", value);
        },
        copyclipboard(){
            var com = this;

            var textToCopy = [];
            for(var link of com.intersectionSet) textToCopy.push(link.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
    },
    mounted(){
        this.emitter.on("copyLayerConnections", () => {
            this.copyclipboard()
        });
    }
}

</script>

<style>
#layer-connect {
    width: 100%;
    height: 100%;
    top: 9.35%;
    position: absolute;
    font-family: 'ABeeZee', sans-serif;
    padding: 0% 2% 2% 2%;
}

#layer-connect .network-results {
    margin-top: 2%;
    height: 78%;
    overflow: scroll;
}
</style>