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
    name: 'PathwayStatistics',
    props: ['active_term'],
    data() {
        return {
            statistics: {}
        }
    },
    watch: {
        active_term(){
            console.log(this.active_term)
            var com = this
            if (com.active_term == null) {

                return;
            }
            const { category, id, fdr_rate, p_value } = com.active_term;
            com.statistics = { category, id, fdr_rate, p_value }

        }
    }
}
</script>

<style>
</style>