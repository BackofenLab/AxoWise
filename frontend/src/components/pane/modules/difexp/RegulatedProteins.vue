<template>
    <div id="de-connect">
        <div class="pane-sorting">
            <a class="pane_attributes" >selection</a>
        </div>

        <div class="selection-results">
            <table >
                <tbody>
                    <tr v-for="(key,entry, index) in selectionattr" :key="index" class="option">
                        <td>
                            <div class="statistics-attr">
                                <a href="#">{{entry}}</a>
                            </div>
                        </td>
                        <td>
                            <input class="statistics-val"
                            type="number"
                            v-bind:min="key.min"
                            v-bind:max="key.max"
                            v-bind:step="key.step"
                            v-model="key.value"
                            v-on:change="select_proteins()"
                            >
                        </td>
                    </tr>
                </tbody>
            </table>
            <!-- <div class="statistics-attr">
                <span>min</span>
                <span>max</span>    
            </div>

            <div class="statistics-val">

                <input
                type="number"
                v-bind:min="maxSelect.min"
                v-bind:max="maxSelect.max"
                v-bind:step="maxSelect.step"
                v-model="maxSelect.value"
                v-on:change="select_proteins()"
                />
            </div> -->
        </div>

        <div class="pane-sorting">
            <a class="pane_attributes" >nodes</a>
            <a class="pane_values">cluster</a>
        </div>

        <div class="network-results" tabindex="0" @keydown="handleKeyDown">
            <table >
                <tbody>
                    <tr v-for="(entry, index) in dvalueNodes" :key="index" class="option">
                        <td>
                            <div class="statistics-attr">
                                <a href="#">{{entry.attributes["Name"]}}</a>
                            </div>
                        </td>
                        <td>
                            <a class="statistics-val">{{entry.attributes["Modularity Class"]}}</a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

export default {
    name: 'RegulatedProteins',
    props: ['active_decoloumn','gephi_data'],
    data() {
        return {
            dvalueNodes: [],
            minSelect: {
                value: -10,
                min: -10,
                max: 0,
                step: 0.1            
            },
            maxSelect: {
                value: 10,
                min: 0,
                max: 10,
                step: 0.1
            },
            selectionattr:{},
        }
    },
    watch: {
        active_decoloumn(){
            var com = this

            com.dvalueNodes = this.gephi_data.nodes
            var dvalue_list = Object.values(com.gephi_data.nodes).map(item => item.attributes[com.active_decoloumn]).filter(value => value !== undefined)
            com.maxSelect.value = Math.max(...dvalue_list)
            com.minSelect.value = Math.min(...dvalue_list)
            com.selectionattr = {max: com.maxSelect, min: com.minSelect}

        }
    },
    methods: {
        select_proteins() {
            this.dvalueNodes = []
            for (var node of this.gephi_data.nodes) {
                var dvalue = node.attributes[this.active_decoloumn]
                if (dvalue >= this.minSelect.value && dvalue <= this.maxSelect.value) this.dvalueNodes.push(node);
            }

            this.emitter.emit("selectDE", this.dvalueNodes);

            },
    }
}
</script>

<style>
#de-connect {
    width: 100%;
    height: 100%;
    top: 8.35%;
    position: absolute;
    font-family: 'ABeeZee', sans-serif;
    padding: 0% 2% 2% 2%;
}

#de-connect .network-results {
    margin-top: 2%;
    height: 58%;
    overflow: scroll;
}

.selection-results{
    margin-top: 2%;
    height: 15%;
    overflow: scroll;
}

.selection-results input[type=number] { 
    border: none;
    width:32%;
    font-family: 'ABeeZee', sans-serif;
    font-size: 0.7vw;
    color: white;
    background: none;
    -moz-appearance: textfield;
    -webkit-appearance: textfield;
    appearance: textfield;
    text-align: left;
}

.selection-results::-webkit-scrollbar {
  display: none;
}

.selection-results table {
    display: flex;
    width: 100%;
}

:focus {outline:0 !important;}

.selection-results table tbody{
    width: 100%;
}
.selection-results td:first-child {
    width: 70%;
    align-self: center;
}
.selection-results td:last-child {
    font-size: 0.7vw;
    margin-bottom: 1%;
    color: white;
    width:  30%;
    align-self: center;
    white-space: nowrap;
    overflow: hidden;    /* Hide overflow content */
    text-overflow: ellipsis;
}
</style>