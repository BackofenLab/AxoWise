<template>
    <div id="statistics">
        <div class="pane-sorting">
            <a class="pane_attributes" >values</a>
            <a class="pane_values">attributes</a>
        </div>

        <div class="network-results" tabindex="0" @keydown="handleKeyDown">
            <table >
                <tbody>
                    <tr v-for="(key, entry, index) in statistics" :key="index" class="option">
                        <td>
                            <div class="statistics-attr">
                                <a href="#">{{key}}</a>
                            </div>
                        </td>
                        <td>
                            <a class="statistics-val">{{entry}}</a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

export default {
    name: 'NetworkStatistics',
    props: ['active_node'],
    data() {
        return {
            statistics: {}
        }
    },
    watch: {
        active_node(){
            var com = this;

            if (com.active_node == null) {
                return;
            }

            const { Degree, "Ensembl ID": EnsemblID } = com.active_node.attributes;
            com.statistics = { Degree, EnsemblID }
            if(com.$store.state.dcoloumns != null) {
                com.$store.state.dcoloumns.forEach(dcoloumn => {
                    com.statistics[dcoloumn] = com.active_node.attributes[dcoloumn]
                });
            }
        }
    }
}
</script>

<style>

#statistics {
    width: 100%;
    height: 100%;
    top: 20.35%;
    position: absolute;
    font-family: 'ABeeZee', sans-serif;
    padding: 0% 2% 2% 2%;
}

.pane-sorting{
    margin-top: 1%;
    margin-left: 1.5%;
    padding-bottom: 0.3%;
    width: 96.5%;
    font-size: 0.5vw;
    border-bottom: 1px solid;
    border-color: white;
    cursor: default;
}
.pane-sorting a {
    color: rgba(255, 255, 255, 0.7);
}

.pane_values{
    position: absolute;
    left: 68.5%;
}

.statistics-attr{
    display: flex;
    height: 1vw;
    width: 92%;
    white-space: nowrap;
    overflow: hidden;    /* Hide overflow content */
    text-overflow: ellipsis;
    margin-left: 2%;
}

.statistics-attr a {
    cursor: default;
    font-size: 0.7vw;
    color: white;
    text-decoration:none;
}

#statistics .network-results {
    margin-top: 2%;
    height: 58%;
    overflow: scroll;
}

.network-results::-webkit-scrollbar {
  display: none;
}

.statistics-val{
    left: 90.6%;
}

.network-results table {
    display: flex;
    width: 100%;
}

:focus {outline:0 !important;}

.network-results table tbody{
    width: 100%;
}
.network-results td:first-child {
    width: 70%;
    align-self: center;
}
.network-results td:last-child {
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