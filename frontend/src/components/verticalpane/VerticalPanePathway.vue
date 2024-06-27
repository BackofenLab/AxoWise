<template>
    <div id="vertical-pane">
        <div class="upper-block">
            <div class="tab-system">
                <ul>
                <li class="tab" :class="{ 'tabSelected': active_function_tab1 === 'list' }" v-on:click="active_function_tab1 = 'list'"><a href="#">list</a></li>
                </ul>
            </div>
            <PathwayGraphMenu
            :term_data='term_data'
            :sorted = '"top"'
            :active_function='active_function_tab1'
            ></PathwayGraphMenu>

        </div>
        <div class="lower-block">
            <div class="tab-system">
                <ul>
                <li class="tab" :class="{ 'tabSelected': active_function_tab2 === 'graph' }" v-on:click="active_function_tab2 = 'graph'"><a href="#">enrichment</a></li>
                </ul>
            </div>
            <PathwayGraphMenu
            :sorted = '"bottom"'
            :term_data='term_data'
            :active_function='active_function_tab2'
            ></PathwayGraphMenu>
        </div>
    </div>
</template>

<script>
import PathwayGraphMenu from '@/components/pathwaytools/PathwayGraphMenu.vue'

export default {
    name: 'VerticalPanePathway',
    props: ['term_data'],
    components: {
        PathwayGraphMenu,
    },
    data() {
        return {
            active_function_tab1: 'list',
            active_function_tab2: 'graph'
        }
    },
    mounted(){

    }
}
</script>

<style>

</style>
