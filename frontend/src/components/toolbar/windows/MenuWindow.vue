<template >
    <div>
        <div class="menu-window">

            <div class="window-label">graph settings</div>
            <div class="menu-items">
                <ToggleLabel
                :mode = 'mode'
                ></ToggleLabel>
                <ConnectedGraph
                :mode = 'mode'
                ></ConnectedGraph>
                <ModuleSelection
                :mode = 'mode'
                ></ModuleSelection>
                <EdgeOpacity
                :mode = 'mode'
                ></EdgeOpacity>
                <NodeLabelSelect
                :mode = 'mode'
                ></NodeLabelSelect>
            </div>
            <div v-if="mode=='protein'">
                <div class="window-label">visualize de-value</div>
                <div class="menu-items">
                    <DEValue></DEValue>
                </div>
            </div>
            <div v-if="mode=='term'">
                <div class="window-label">visualize fdr-rate</div>
                <div class="menu-items">
                    <FDRValue></FDRValue>
                </div>
            </div>
            <div class="window-label">export graph</div>
            <div class="menu-items">
                <ExportScreen
                :mode = 'mode'
                ></ExportScreen>
                <ExportGraph v-if="mode=='protein'"
                ></ExportGraph>
                <ExportProteins v-if="mode=='protein'"
                :gephi_data = 'gephi_data'
                ></ExportProteins>
                <ExportEdges v-if="mode=='protein'"
                :gephi_data = 'gephi_data'
                :ensembl_name_index = 'ensembl_name_index'
                ></ExportEdges>
            </div>
        </div>
    </div>
</template>

<script>

import ExportProteins from '@/components/toolbar/modules/ExportProteins.vue'
import ExportEdges from '@/components/toolbar/modules/ExportEdges.vue'
import ExportScreen from '@/components/toolbar/modules/ExportScreen.vue'
import DEValue from '@/components/toolbar/modules/DEValue.vue'
import FDRValue from '@/components/toolbar/modules/FDRValue.vue'
import ExportGraph from '@/components/toolbar/modules/ExportGraph.vue'
import NodeLabelSelect from '@/components/toolbar/modules/NodeLabelSelect.vue'
import ConnectedGraph from '@/components/toolbar/modules/ConnectedGraph.vue'
import ToggleLabel from '@/components/toolbar/modules/ToggleLabel.vue'
import EdgeOpacity from '@/components/toolbar/modules/EdgeOpacity.vue'
import ModuleSelection from '@/components/toolbar/modules/ModuleSelection.vue'

export default {
    name: 'MenuWindow',
    props: ['tools_active','mode','gephi_data','ensembl_name_index'],
    emits:['tools_active_changed'],
    components: {
        ExportScreen,
        DEValue,
        ExportGraph,
        EdgeOpacity,
        NodeLabelSelect,
        ConnectedGraph,
        ToggleLabel,
        ModuleSelection,
        FDRValue,
        ExportProteins,
        ExportEdges

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
    top: 4.98%;
    padding: 0.3% 0 0.3% 0;
    border-radius: 0 0 5px 5px;
    background: rgba(222, 222, 222, 0.61);
	overflow-y: scroll;
	overflow-x: hidden;
	color: white;
    border-top-color: rgba(255, 255, 255, 30%);
    border-top-width: 1px;
    border-top-style: solid;
    cursor: default;
    z-index: 1;
}

.menu-window:after {
    content:"";
    position:absolute;
    z-index: -1;
    top:0;
    left:0;
    width:100%;
    height:100%;
    backdrop-filter: blur(7.5px);
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
