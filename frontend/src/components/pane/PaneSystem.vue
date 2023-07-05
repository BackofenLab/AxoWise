<template>
    <div id="attributepane" class="pane" v-show="active_node !== null || active_subset !== null || active_term !== null || active_decoloumn !== null || active_termlayers !== null ||paneHidden == false">
        <div class="buttons">
            <button id="panebutton" v-on:click="open_pane()">
                <img id="collapse-icon" src="@/assets/toolbar/winkel-rechts.png" alt="Collapse Icon">
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
            :gephi_data='gephi_data'
            @active_item_changed = 'active_item = $event'
            ></NodePane>
            <TermPane v-show="active_tab === 'term'" 
            :active_term='active_term' 
            :gephi_data='gephi_data'
            @active_item_changed = 'active_item = $event'
            @highlight_subset_changed = 'highlight_subset = $event'
            ></TermPane>
            <SubsetPane v-show="active_tab === 'subset'"
            :active_subset='active_subset'
            :gephi_data='gephi_data'
            @active_item_changed = 'active_item = $event'
            @highlight_subset_changed = 'highlight_subset = $event'
            @active_layer_changed = 'active_layer = $event'
            ></SubsetPane>
            <DEValuePane v-show="active_tab === 'devalue'"
            :active_decoloumn='active_decoloumn'
            :gephi_data='gephi_data'
            @active_item_changed = 'active_item = $event'
            ></DEValuePane>
            <EnrichmentLayerPane v-show="active_tab === 'layers'"
            :active_termlayers='active_termlayers'
            :gephi_data='gephi_data'
            @active_item_changed = 'active_item = $event'
            ></EnrichmentLayerPane>
        </div>
    </div>
</template>

<script>

import NodePane from '@/components/pane/NodePane.vue'
import TermPane from '@/components/pane/TermPane.vue'
import SubsetPane from '@/components/pane/SubsetPane.vue'
import DEValuePane from '@/components/pane/DEValuePane.vue'
import EnrichmentLayerPane from '@/components/pane/EnrichmentLayerPane.vue'

export default {
    name:"PaneSystem",
    props:['gephi_data', 'active_subset', 'active_term', 'active_node', 'active_decoloumn','active_termlayers', 'node_color_index'],
    emits:['active_node_changed','active_term_changed', 'active_subset_changed', 'active_combine_changed', 'active_layer_changed', 'active_termlayers_changed'],
    components: {
        NodePane,
        TermPane,
        SubsetPane,
        DEValuePane,
        EnrichmentLayerPane
    },
    data() {
        return{
            active_item: null,
            active_dict: {},
            active_tab: "node",
            highlight_subset: null,
            paneHidden: true
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
        }


    },
    methods: {
        open_pane(){
            const div = document.getElementById('attributepane');
            const paneButton = document.getElementById('panebutton');
            const paneCloseButton = document.getElementById('paneclosebutton');
            const collapseIcon = document.getElementById('collapse-icon');

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
                this.$emit('active_termlayers_changed', null)
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
            this.$emit('active_term_changed', null)
            this.$emit('active_subset_changed', null)
            this.$emit('active_layer_changed', null)
            this.$emit('active_decoloumn_changed', null)
            this.$emit('active_termlayers_changed', null)
            this.emitter.emit('enrichTerms', null)
            this.emitter.emit('enrichSubset', null)

        },
        selectTab(name, tab){
            if(name == "node"){
                this.active_tab = "node"
                this.$emit('active_node_changed', null)
                this.$emit('active_combine_changed', {value: tab, name: name})
            }
            if(name == "term"){
                this.active_tab = "term"
                this.$emit('active_term_changed', null)
                this.$emit('active_combine_changed', {value: tab, name: name})
            }
            if(name == "subset"){
                this.active_tab = "subset"
                this.$emit('active_subset_changed', null)
                this.$emit('active_combine_changed', {value: tab, name: name})
            }
            if(name == "devalue"){
                this.active_tab = "devalue"
                this.$emit('active_decoloumn_changed', null)
                this.$emit('active_combine_changed', {value: tab, name: name})
            }
            if(name == "layers"){
                this.active_tab = "layers"
                console.log(name, tab)
                this.$emit('active_termlayers_changed', null)
                this.$emit('active_combine_changed', {value: tab, name: name})
            }
        }
    },
    mounted(){
        this.emitter.on("reset_protein",(state) => {
            this.selectTab("node",state)
        })

        }
}
</script>

<style>
.buttons button img {
    width: 10px;
    filter: invert(1);
}
.rotate {
  transform: rotate(180deg);
}
.tabs button {
    margin-top: 10px;
}

.buttons .tabs button img{
    width: 20px;
}
</style>