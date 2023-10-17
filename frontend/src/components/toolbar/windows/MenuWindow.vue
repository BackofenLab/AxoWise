<template >
    <div>
        <div class="menu-window" 
            v-on:mouseleave="active_window(false);"
            v-on:mouseover="active_window(true);">

            <div class="window-label">graph settings</div>
            <div class="menu-items">
                <NodeLabelSelect
                :type="screen_type"
                ></NodeLabelSelect>
                <!-- <EdgeOpacity></EdgeOpacity> -->
            </div>
            <div class="window-label">visualize de-value</div>
            <div class="menu-items">
                <!-- <DEValue></DEValue> -->
            </div>
            <div class="window-label">export graph</div>
            <div class="menu-items">
                <ExportScreen
                :type="screen_type"
                ></ExportScreen>
                <ExportGraph></ExportGraph>
            </div>
        </div>
    </div>
</template>

<script>

import ExportScreen from '@/components/toolbar/modules/ExportScreen.vue'
// import DEValue from '@/components/toolbar/DEValue.vue'
import ExportGraph from '@/components/toolbar/modules/ExportGraph.vue'
import NodeLabelSelect from '@/components/toolbar/modules/NodeLabelSelect.vue'
// import EdgeOpacity from '@/components/toolbar/EdgeOpacity.vue'

export default {
    name: 'MenuWindow',
    props: ['tools_active'],
    emits:['tools_active_changed'],
    components: {
        ExportScreen,
        // DEValue,
        ExportGraph,
        // EdgeOpacity,
        NodeLabelSelect

    },
    data() {
        return {
        }
    },
    methods: {
        active_window(state) {
            this.$emit("tools_active_changed", state);
        }
    }
}
</script>

<style>

.menu-window {
    position: absolute;
    left: 3.515%;
    height: fit-content;
    width: 22%;
    top: 5.78%;
    padding: 0.3% 0 0.3% 0;
    border-radius: 0 0 5px 5px;
    background: rgba(222, 222, 222, 0.61);
    backdrop-filter: blur(7.5px);
	overflow-y: scroll;
	overflow-x: hidden;
	color: white;
    border-top-color: rgba(255, 255, 255, 30%);
    border-top-width: 1px;
    border-top-style: solid;
}

.menu-items {
    margin: 1% 0 1% 6%;
    width: 100%;
    color:  white;
}

.window-label {
    margin-left: 3%;
    width: 93%;
    font-family: 'ABeeZee', sans-serif;
    color: rgba(255, 255, 255, 50%);
    font-size: 0.9vw;
    border-bottom: 1px solid;
    border-color: rgba(255, 255, 255, 50%);
    cursor: default;
}

.tool-item {
    font-family: 'ABeeZee', sans-serif;
    font-size: 1vw;

}

</style>
