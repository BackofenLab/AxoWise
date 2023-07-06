<template>
    <div id="attributepane" class="pane" v-show="active_node !== null || active_fdr !== null || active_subset !== null || paneHidden == false">
        <div class="buttons">
            <button id="panebutton" v-on:click="open_pane()">
                <img id="term-collapse-icon" src="@/assets/toolbar/winkel-rechts.png" alt="Collapse Icon">
            </button>
            <button id="paneclosebutton" v-on:click="close_pane()">
                <img src="@/assets/toolbar/cross.png" alt="Close Icon">
            </button>
            <div class="tabs">
                <button v-for="(tab, name) in active_dict" :key="name" @click="selectTab(name,tab.value)">
                    <img :src="tab.imageSrc" class="tab_button">
                </button>
            </div>
        </div>
        <div class="main-section">
            <NodePane v-show="active_tab === 'node'"
            :active_node='active_node' 
            :node_color_index='node_color_index'
            :term_data='term_data'
            @active_item_changed = 'active_item = $event'
            ></NodePane>
            <TermSubsetPane v-show="active_tab === 'subset'"
            :active_subset='active_subset'
            @active_item_changed = 'active_item = $event'
            @highlight_subset_changed = 'highlight_subset = $event'
            @active_layer_changed = 'active_layer = $event'
            ></TermSubsetPane>
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
import TermSubsetPane from '@/components/term_graph/TermSubsetPane.vue'

export default {
    name:"TermPaneSystem",
    props:['term_data', 'active_node','active_fdr', 'node_color_index','active_subset'],
    emits:['active_node_changed', 'active_fdr_changed', 'active_combine_changed', 'active_subset_changed'],
    components: {
        NodePane,
        FDRPane,
        TermSubsetPane
    },
    data() {
        return{
            active_item: null,
            active_dict: {},
            active_tab: "node",
            paneHidden: true,
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
            const collapseIcon = document.getElementById('term-collapse-icon');

            if (!div.classList.contains('pane-show')) {
                div.classList.add('pane-show');
                paneButton.style.height = '100%';
                paneCloseButton.style.visibility = 'hidden';
                collapseIcon.classList.add('rotate');

                this.paneHidden = false;

                this.$emit('active_node_changed', null)
                this.$emit('active_term_changed', null)
                this.$emit('active_subset_changed', null)
                this.$emit('active_layer_changed', null)
                this.$emit('active_decoloumn_changed', null)
                this.emitter.emit('enrichTerms', null)
                this.emitter.emit('enrichSubset', null)
            } else {
                div.classList.remove('pane-show');
                paneCloseButton.style.visibility = 'visible';
                paneButton.style.height = '25px';
                collapseIcon.classList.remove('rotate');
                this.paneHidden = true
                var nameKey = Object.keys(this.active_dict)[0]
                this.selectTab(nameKey, this.active_dict[nameKey].value)
            }
        },
        close_pane(){

            this.active_dict = {}

            this.$emit('active_node_changed', null)
            this.$emit('active_fdr_changed', null)
            this.$emit('active_subset_changed', null)

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
            if(name == "subset"){
                this.active_tab = "subset"
                this.$emit('active_subset_changed', null)
                this.$emit('active_combine_changed', {value: tab, name: name})
            }
        }
    }
}
</script>

<style>
</style>