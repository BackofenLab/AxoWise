<template>
    <div id="statistics">
        <div class="pane-sorting">
            <a class="pane_attributes" >nodes</a>
            <a class="pane_values">cluster</a>
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
    name: 'NodeConnections',
    props: ['active_node'],
    data() {
        return {
        }
    },
}
</script>

<style>
</style>