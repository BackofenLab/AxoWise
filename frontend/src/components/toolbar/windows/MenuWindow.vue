<template >
    <div>
        <div class="menu-window">

            <div class="window-label">graph settings</div>
            <div class="menu-items">
                <ToggleLabel></ToggleLabel>
                <ConnectedGraph></ConnectedGraph>
                <EdgeOpacity></EdgeOpacity>
                <NodeLabelSelect
                :type="screen_type"
                ></NodeLabelSelect>
            </div>
            <div class="window-label">visualize de-value</div>
            <div class="menu-items">
                <DEValue></DEValue>
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
import DEValue from '@/components/toolbar/modules/DEValue.vue'
import ExportGraph from '@/components/toolbar/modules/ExportGraph.vue'
import NodeLabelSelect from '@/components/toolbar/modules/NodeLabelSelect.vue'
import ConnectedGraph from '@/components/toolbar/modules/ConnectedGraph.vue'
import ToggleLabel from '@/components/toolbar/modules/ToggleLabel.vue'
import EdgeOpacity from '@/components/toolbar/modules/EdgeOpacity.vue'

export default {
    name: 'MenuWindow',
    props: ['tools_active'],
    emits:['tools_active_changed'],
    components: {
        ExportScreen,
        DEValue,
        ExportGraph,
        EdgeOpacity,
        NodeLabelSelect,
        ConnectedGraph,
        ToggleLabel

    },
    data() {
        return {
        }
    },
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
    display: flex;

}

</style>
