<template>
    <div id="vertical-pane">
        <div class="upper-block">
            <div class="tab-system">
                <ul>
                <li class="tab" :class="{ 'tabSelected': active_function_tab1 === 'list' }" v-on:click="active_function_tab1 = 'list'"><a href="#">list</a></li>
                </ul>
            </div>
            <CitationList
            :citation_data='citation_data'
            :sorted = '"top"'
            ></CitationList>

        </div>
        <div class="lower-block">
            <div class="tab-system">
                <ul>
                <li class="tab" :class="{ 'tabSelected': active_function_tab2 === 'summary' }" v-on:click="active_function_tab2 = 'summary'"><a href="#">summary</a></li>
                </ul>
            </div>
            <CitationSummary
            :citation_data='citation_data'
            :sorted = '"bottom"'
            ></CitationSummary>

        </div>
    </div>
</template>

<script>
import CitationList from '@/components/citation/CitationList.vue'
import CitationSummary from '@/components/citation/CitationSummary.vue'

export default {
    name: 'VerticalPaneCitation',
    props: ['citation_data'],
    components: {
        CitationList,
        CitationSummary
    },
    data() {
        return {
            active_function_tab1: 'list',
            active_function_tab2: 'summary'
        }
    },
}
</script>

<style>

</style>
