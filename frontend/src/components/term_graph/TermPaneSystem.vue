<template>
    <div id="attributepane" class="pane" v-show="active_node !== null || active_fdr !== null">
        <div class="buttons">
            <button id="panebutton" v-on:click="open_pane()"></button>
            <button id="paneclosebutton" v-on:click="close_pane()"></button>
            <div class="tabs">
                <button v-for="(tab, name) in active_dict" :key="name" @click="selectTab(name,tab)"></button>
            </div>
        </div>
        <div class="main-section">
            <NodePane v-show="active_node !== null"
            :active_node='active_node' 
            :node_color_index='node_color_index'
            :term_data='term_data'
            @active_item_changed = 'active_item = $event'
            ></NodePane>
            <FDRPane v-show="active_fdr !== null"
            :term_data='term_data'
            @active_item_changed = 'active_item = $event'
            ></FDRPane>
        </div>
    </div>
</template>

<script>

import NodePane from '@/components/term_graph/TermNodePane.vue'
import FDRPane from '@/components/term_graph/FDRPane.vue'

export default {
    name:"TermPaneSystem",
    props:['term_data', 'active_node','active_fdr', 'node_color_index'],
    emits:['active_node_changed', 'active_fdr_changed'],
    components: {
        NodePane,
        FDRPane
    },
    data() {
        return{
        }
    },
    watch: {
    },
    methods: {
        open_pane(){
            const div = document.getElementById('attributepane');
            const paneButton = document.getElementById('panebutton');
            const paneCloseButton = document.getElementById('paneclosebutton');

            if (!div.classList.contains('pane-show')) {
                div.classList.add('pane-show');
                paneButton.style.height = '100%';
                paneCloseButton.style.visibility = 'hidden';
            } else {
                div.classList.remove('pane-show');
                paneCloseButton.style.visibility = 'visible';
                paneButton.style.height = '25px';
            }
        },
        close_pane(){

            this.active_dict = {}

            this.$emit('active_node_changed', null)
            this.$emit('active_fdr_changed', null)

        },
    }
}
</script>

<style>
</style>