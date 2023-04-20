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
            <NodePane v-show="active_tab === 'node'"
            :active_node='active_node' 
            :node_color_index='node_color_index'
            :term_data='term_data'
            @active_item_changed = 'active_item = $event'
            ></NodePane>
            <FDRPane v-show="active_tab === 'fdr'"
            :term_data='term_data'
            :active_fdr='active_fdr'
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
    emits:['active_node_changed', 'active_fdr_changed', 'active_combine_changed'],
    components: {
        NodePane,
        FDRPane
    },
    data() {
        return{
            active_item: null,
            active_dict: {},
            active_tab: "node",
        }
    },
    watch: {
        active_item(val){
            this.active_tab = Object.keys(val)[0]
            if(val == null){
                delete this.active_dict.val;
                return
            }
            Object.assign(this.active_dict, val);
        },
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
        selectTab(name, tab){
            if(name == "node"){
                this.active_tab = "node"
                this.$emit('active_node_changed', null)
                this.$emit('active_combine_changed', {value: tab, name: name})
            }
            if(name == "fdr"){
                this.active_tab = "fdr"
                this.$emit('active_fdr_changed', null)
                this.$emit('active_combine_changed', {value: tab, name: name})
            }
        }
    }
}
</script>

<style>
</style>