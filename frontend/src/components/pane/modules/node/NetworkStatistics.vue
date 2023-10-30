<template>
    <div id="statistics">
        <div class="pane-sorting">
            <a class="pane_attributes" >attributes</a>
            <a class="pane_values">values</a>
        </div>

        <div class="network-results" tabindex="0" @keydown="handleKeyDown">
            <table >
                <tbody>
                    <!-- <tr v-for="(entry, index) in active_node.attributes" :key="index" class="option">
                        <td>
                            <div class="statistics-attr">
                                <a href="#">{{entry}}</a>
                            </div>
                        </td>
                        <td>
                            <a class="statistics-val">{{ entry}}</a>
                        </td>
                    </tr> -->
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
        }
    },
}
</script>

<style>

#statistics {
    width: 100%;
    top: 16.35%;
    position: absolute;
    padding: 0% 2% 2% 2%;
}

.pane-sorting{
    margin-top: 1%;
    padding-bottom: 0.3%;
    width: 99%;
    font-size: 0.5vw;
    border-bottom: 1px solid;
    border-color: white;
    cursor: default;
}
.pane-sorting a {
    color: rgba(255, 255, 255, 0.7);
}

.pane_values{
    position: fixed;
    left: 90.6%;
}

.list-section .results {
    height: 90%;
    overflow: scroll;
}
</style>