<template>
    <div id="pathway-connect">
        <div class="pane-sorting">
            <a class="pane_attributes" >nodes</a>
            <a class="pane_values">cluster</a>
        </div>

        <div class="network-results" tabindex="0" @keydown="handleKeyDown">
            <table >
                <tbody>
                    <tr v-for="(entry, index) in links" :key="index" class="option">
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
    name: 'PathwayConnections',
    props: ['active_term','gephi_data'],
    data() {
        return {
            links: []
        }
    },
    watch: {
        active_term(){
            var com = this

            if (com.active_term == null) {
                return;
            }
            const activeTermProteins = new Set(com.active_term.symbols);
            com.links = com.gephi_data.nodes.filter(node => activeTermProteins.has(node.attributes['Name']));
        }
    }
}
</script>

<style>
#pathway-connect {
    width: 100%;
    height: 100%;
    top: 8.35%;
    position: absolute;
    font-family: 'ABeeZee', sans-serif;
    padding: 0% 2% 2% 2%;
}

#pathway-connect .network-results {
    margin-top: 2%;
    height: 81%;
    overflow: scroll;
}
</style>