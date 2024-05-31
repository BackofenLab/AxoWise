<template>
    <div id="vertical-pane">
        <SearchField
        :data='gephi_data'
        ></SearchField>
        <div class="upper-block">
            <div class="tab-system">
                <ul>
                <li class="tab" :class="{ 'tabSelected': active_function_tab1 === 'set' }" v-on:click="active_function_tab1 = 'set'"><a href="#">term set</a></li>
                <li class="tab" :class="{ 'tabSelected': active_function_tab1 === 'layers' }" v-on:click="active_function_tab1 = 'layers'"><a href="#">path layers</a></li>
                <li class="tab" v-if="dcoloumns" :class="{ 'tabSelected': active_function_tab1 === 'difexp' }" v-on:click="active_function_tab1 = 'difexp'"><a href="#">dif exp</a></li>
                </ul>
            </div>
            <PathwayMenu
            :gephi_data='gephi_data'
            :sorted = '"top"'
            :active_function='active_function_tab1'
            @active_term_changed = 'active_term = $event'
            @active_layer_changed = 'active_layer = $event'
            ></PathwayMenu>

            <PathwayLayers 
            v-show="active_function_tab1=='layers'"
            :active_termlayers='active_termlayers'
            :gephi_data='gephi_data'
            ></PathwayLayers>

            <DifExpMenu 
            v-show="active_function_tab1=='difexp'"
            :active_decoloumn='active_decoloumn'
            :gephi_data='gephi_data'
            ></DifExpMenu>
        </div>
        <div class="lower-block">
            <div class="tab-system">
                <ul>
                <li class="tab" :class="{ 'tabSelected': active_function_tab2 === 'list' }" v-on:click="active_function_tab2 = 'list'"><a href="#">pathways</a></li>
                <li class="tab" :class="{ 'tabSelected': active_function_tab2 === 'graph' }" v-on:click="active_function_tab2 = 'graph'"><a href="#">graphs</a></li>
                <li class="tab" :class="{ 'tabSelected': active_function_tab2 === 'heatmap' }" v-on:click="active_function_tab2 = 'heatmap'"><a href="#">heatmap</a></li>
                <li class="tab" :class="{ 'tabSelected': active_function_tab2 === 'citation' }" v-on:click="active_function_tab2 = 'citation'"><a href="#">citation</a></li>
                </ul>
            </div>
            <PathwayMenu v-show="active_function_tab2==='list' || active_function_tab2==='graph' || active_function_tab2==='heatmap'"
            :sorted = '"bottom"'
            :gephi_data='gephi_data'
            :active_function='active_function_tab2'
            @active_term_changed = 'active_term = $event'
            @active_layer_changed = 'active_layer = $event'
            ></PathwayMenu>
            <CitationMenu v-show="active_function_tab2==='citation'"
            :sorted = '"bottom"'
            :active_function='active_function_tab2'
            :active_node='active_node'
            ></CitationMenu>
        </div>
    </div>
</template>

<script>
import PathwayMenu from '@/components/enrichment/PathwayMenu.vue'
import CitationMenu from '@/components/citation/CitationMenu.vue'
import SearchField from '@/components/interface/SearchField.vue'
import PathwayLayers from '@/components/pane/modules/layer/PathwayLayers.vue'
import DifExpMenu from '@/components/pane/modules/difexp/DifExpMenu.vue'

export default {
    name: 'VerticalPane',
    props: ['gephi_data','active_node','active_termlayers','active_decoloumn'],
    components: {
        PathwayMenu,
        SearchField,
        PathwayLayers,
        DifExpMenu,
        CitationMenu
    },
    data() {
        return {
            dcoloumns:this.$store.state.dcoloumns,
            active_function_tab1: 'set',
            active_function_tab2: 'list'
        }
    },
    mounted(){

    }
}
</script>

<style>
#vertical-pane{
    left: 0;
    top: 0;
    height: 100%;
    width:25vw;
    background: #0A0A1A;
    -webkit-backdrop-filter: blur(7.5px);
    padding: 1%;
}

.upper-block{
    height: 45%;
    top: 0%;
    position: relative;
    border-style: solid;
    border-width: 1px;
    border-color: white;
    margin-top: 2%;
    overflow: hidden;
}

.lower-block{
    margin-top: 2%;
    height: 48%;
    position: relative;
    overflow: hidden;
    border-style: solid;
    border-width: 1px;
    border-color: white;
}

 ul {
  display: inline-block;
  width: 100%;
  list-style-type: none;
}

.tab-system a {
  font-size: 0.8vw;
  font-family: 'ABeeZee', sans-serif;
  text-decoration: none;
  color: white;
}

.tab {
  float: left;
  display: flex;
  height: 10%;
  padding: 0 3% 1% 3%;
  border-right: 0.1vw solid white;
  overflow: hidden;
}

.tab, .tab a {
  transition: all .25s;
}

.tab a {
  display: inline-block;
}

.tab a:first-child {
  padding: 1%;
  white-space: nowrap;
}

.tab:hover {
    background: rgba(222, 222, 222, 0.71);;
}

.tabSelected {
    position: relative;
}
.tabSelected:before {
  content : "";
  position: absolute;
  left    : 50%;
  bottom  : 0;
  width   : 90%;
  transform: translateX(-50%);
  border-bottom: 0.15vw solid #e6eaf5;
}

</style>
