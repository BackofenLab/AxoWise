<template>
    <div v-show="active_node !== null || active_subset !== null ||paneHidden == false">
    <div id="attributepane" class="pane">
        <div class="headertext">
            <span>{{active_tab}}</span>
            <img  class="pane_close" src="@/assets/pathwaybar/cross.png" v-on:click="close_pane()">
        </div>
    </div>
    <div class="pane-window">
        <PathwayPane v-show="active_tab === 'Protein'"
            :mode = 'mode'
            :active_node='active_node' 
            :node_color_index='node_color_index'
            :gephi_data='gephi_data'
            @active_item_changed = 'active_item = $event'
        ></PathwayPane>
        <SubsetPane v-show="active_tab === 'Subset'"
            :mode = 'mode'
            :active_subset='active_subset'
            :gephi_data='gephi_data'
            @active_item_changed = 'active_item = $event'
            @highlight_subset_changed = 'highlight_subset = $event'
            @active_layer_changed = 'active_layer = $event'
        ></SubsetPane>
    </div>
    </div>
</template>

<script>

import PathwayPane from '@/components/pane/modules/pathway/PathwayPane.vue'
import SubsetPane from '@/components/pane/modules/subset/SubsetPane.vue'

export default {
    name:"TermPaneSystem",
    props:['gephi_data', 'active_subset', 'active_node', 'node_color_index'],
    emits:['active_node_changed', 'active_subset_changed', 'active_combine_changed', 'active_layer_changed'],
    components: {
        PathwayPane,
        SubsetPane,
    },
    data() {
        return{
            active_item: null,
            active_dict: {},
            active_tab: "Protein",
            highlight_subset: null,
            paneHidden: true,
            mode: "term"
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
        close_pane(){

            this.active_dict = {}

            this.$emit('active_node_changed', null)
            this.$emit('active_subset_changed', null)
            this.$emit('active_layer_changed', null)

        },
        selectTab(name, tab){
            if(name == "node"){
                this.active_tab = "node"
                this.$emit('active_node_changed', null)
                this.$emit('active_combine_changed', {value: tab, name: name})
            }
            if(name == "subset"){
                this.active_tab = "subset"
                this.$emit('active_subset_changed', null)
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

</style>