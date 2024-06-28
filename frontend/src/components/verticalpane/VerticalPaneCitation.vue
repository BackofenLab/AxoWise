<template>
    <div id="vertical-pane">
        <div class="upper-block">
            <div class="tab-system">
                <ul>
                <li class="tab" :class="{ 'tabSelected': active_function_tab1 === 'list' }" v-on:click="active_function_tab1 = 'list'"><a href="#">list</a></li>
                <li class="tab" :class="{ 'tabSelected': active_function_tab1 === 'clist' }" v-on:click="active_function_tab1 = 'clist'"><a href="#">communities</a></li>
                </ul>
            </div>
            <CitationList v-show="active_function_tab1 === 'list'"
            :citation_data='citation_data'
            :sorted = '"top"'
            ></CitationList>
            <CitationCommunities v-show="active_function_tab1 === 'clist'"
            :citation_data='citation_data'
            :sorted = '"top"'
            :await_community = 'await_community'
            ></CitationCommunities>

        </div>
        <div class="lower-block">
            <div class="tab-system">
                <ul>
                <li class="tab" :class="{ 'tabSelected': active_function_tab2 === 'summary' }" v-on:click="active_function_tab2 = 'summary'"><a href="#">summary</a></li>
                </ul>
            </div>
            <CitationSummary
            :citation_data='citation_data'
            :node_index='node_index'
            :await_community = 'await_community' @await_community_changed = 'await_community = $event'
            :sorted = '"bottom"'
            ></CitationSummary>

        </div>
    </div>
</template>

<script>
import CitationList from '@/components/citation/CitationList.vue'
import CitationCommunities from '@/components/citation/CitationCommunities.vue'
import CitationSummary from '@/components/citation/CitationSummary.vue'

export default {
    name: 'VerticalPaneCitation',
    props: ['citation_data','node_index'],
    components: {
        CitationList,
        CitationSummary,
        CitationCommunities
    },
    data() {
        return {
            active_function_tab1: 'list',
            active_function_tab2: 'summary',
            await_community: false
        }
    },
}
</script>

<style>

</style>
