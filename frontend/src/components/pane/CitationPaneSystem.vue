<template>
    <div v-show="active_subset !== null && active_node == null || paneHidden == false">
        <div class="pane" id="pane" :class="{'active': tool_active}">
            <div class="pane_header"  id="pane_header">
                <span>{{active_tab}}</span>
                <img  class="abstract_add" src="@/assets/pathwaybar/plus.png" v-on:click="add_subset(active_subset)">
                <img  class="pane_close" src="@/assets/toolbar/cross.png" v-on:click="close_pane()">
            </div>
            <div class="pane-window">
                <SubsetPane v-show="active_tab === 'Subset'"
                    :mode = 'mode'
                    :tool_active = 'tool_active'
                    @tool_active_changed = 'tool_active = $event'
                    :active_subset='active_subset'
                    :gephi_data='gephi_data'
                    @active_item_changed = 'active_item = $event'
                    @highlight_subset_changed = 'highlight_subset = $event'
                    @active_layer_changed = 'active_layer = $event'
                ></SubsetPane>
            </div>
        </div>
    </div>
</template>

<script>

import SubsetPane from '@/components/pane/modules/subset/SubsetPane.vue'

export default {
    name:"TermPaneSystem",
    props:['gephi_data', 'active_subset', 'active_node', 'node_color_index'],
    emits:['active_node_changed', 'active_subset_changed', 'active_combine_changed', 'active_layer_changed'],
    components: {
        SubsetPane,
    },
    data() {
        return{
            active_item: null,
            active_dict: {},
            active_tab: "Subset",
            highlight_subset: null,
            paneHidden: true,
            mode: "citation",
            tool_active: false
        }
    },
    watch: {
        active_item(val){
            this.$emit('active_node_changed', null)
            if(this.active_tab != Object.keys(val)[0]) this.tool_active = false;
            this.active_tab = Object.keys(val)[0]
            if(val == null){
                delete this.active_dict.val;
                return
            }
            Object.assign(this.active_dict, val);
        }

    },
    methods: {
        dragElement(elmnt) {
            var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
            if (document.getElementById(elmnt.id + "_header")) {
                // if present, the header is where you move the DIV from:
                document.getElementById(elmnt.id + "_header").onmousedown = dragMouseDown;
            } else {
                // otherwise, move the DIV from anywhere inside the DIV: 
                elmnt.onmousedown = dragMouseDown;
            }

            function dragMouseDown(e) {
                e = e || window.event;
                e.preventDefault();
                // get the mouse cursor position at startup:
                pos3 = e.clientX;
                pos4 = e.clientY;
                document.onmouseup = closeDragElement;
                // call a function whenever the cursor moves:
                document.onmousemove = elementDrag;
            }

            function elementDrag(e) {
                e = e || window.event;
                e.preventDefault();
                // calculate the conditions:
                var parentWidth = window.innerWidth;
                var parentHeight = window.innerHeight;
                var elementWidth = elmnt.offsetWidth;
                var elementHeight = elmnt.offsetHeight;

                // calculate the new coordinates:
                pos1 = pos3 - e.clientX;
                pos2 = pos4 - e.clientY;
                pos3 = e.clientX;
                pos4 = e.clientY;

                // Calculate the new coordinates for bottom and right
                var newBottom = parentHeight - (elmnt.offsetTop - pos2 + elementHeight);
                var newRight = parentWidth - (elmnt.offsetLeft - pos1 + elementWidth);


                // set the element's new position:
                elmnt.style.bottom = newBottom + "px";
                elmnt.style.right = newRight + "px";
            }

            
            function closeDragElement() {
                // stop moving when mouse button is released:
                document.onmouseup = null;
                document.onmousemove = null;
            }
        },
        close_pane(){

            this.active_dict = {}

            if(this.active_node == null) 
            {
                this.$emit('active_subset_changed', null)
                this.$emit('active_layer_changed', null)
            }

        },
        add_subset(subset){
            console.log(subset)
            this.emitter.emit('addSubsetToSummary', subset)
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
        this.dragElement(document.getElementById("pane"));

        this.emitter.on("reset_protein",(state) => {
            this.selectTab("node",state)
        })
    }
}
</script>

<style>

</style>