<template>
    <div id="subset-connect">
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
    name: 'SubsetConnections',
    props: ['active_subset'],
    data() {
        return {
            links: []
        }
    },
    watch: {
        active_subset(){
            var com = this

            if (com.active_subset == null) {
                return;
            }

            com.links = com.active_subset

        }
    }
}
</script>

<style>
#subset-connect {
    width: 100%;
    height: 100%;
    top: 8.35%;
    position: absolute;
    font-family: 'ABeeZee', sans-serif;
    padding: 0% 2% 2% 2%;
}

#subset-connect .network-results {
    margin-top: 2%;
    height: 82%;
    overflow: scroll;
}
</style>