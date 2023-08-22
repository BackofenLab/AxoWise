<template>
    <div id="layerpane" class="text" v-if="active_termlayers !== null">
        <div class="headertext">
            <span>Term Visualization</span>
        </div>
        <button id="hide-btn" class="subset-btn" v-on:click="show_layer()">Hide</button>
        <div class="change-level-menu">
            <button id="apply-func-btn" class="subset-btn" v-on:click="apply_func(true)">Apply</button>
            <button id="revert-func-btn" class="subset-btn" v-on:click="apply_func(false)">Revert</button>
        </div>
        <div class="nodeattributes">
            <div class="p">
            <span>Layers:</span>
            </div>
            <div class="link-enrichment">
                <ul>
                    <li class="membership" v-for="(term) in terms" :key="term" >
                        <div class="color-rect" @click="open_picker($event,term)" :style="{ backgroundColor: colorpalette[term.name] }"></div>
                        <button id="hide-termlayer" @click="hide_termlayer(term)" :class="{ hide: hiding_terms.has(term) }">
                            <img :src="imageSrc" class="hide_button"></button>
                        <a href="#" v-on:click="select_enrichment(term)" @mouseenter="prehighlight(term.proteins)" @mouseleave="prehighlight(null)">{{term.name}}</a>
                    </li>
                </ul>
                <Sketch id="color-picker" v-if="color_picker==true" v-model="colors" @update:model-value="handleColorChange(term)" :style="{ top: mouseY + 'px', left: mouseX + 'px' }" />
            </div>
            <div class="p">
                <span>Connections:</span>
                <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
                <button v-on:click="expand_proteins=!expand_proteins" id="expand-btn">Expand</button>
            </div>
            <div class="link" id="highlighted_proteins" v-show="expand_proteins === true">
                <ul>
                    <li class="membership" v-for="protein in intersectionSet" :key="protein" >
                        <a href="#" v-on:click="select_node(protein)" @mouseenter="prehighlight([protein])" @mouseleave="prehighlight(null)">{{protein.attributes["Name"]}}</a>
                    </li>
                </ul>
            </div>
            <div class="p2">
                <b>Links:</b>
                <button v-on:click="expand_links=!expand_links" id="expand-btn">Expand</button>
                </div>
                    <div class="link" id="edges" v-show="expand_links === true">
                        <ul>
                            <li v-for="edge in intersectingDicts" :key="edge">
                                <div class="edge">
                                <a href="#" >{{edge[0].name}}</a>
                                <a href="#" >{{edge[1].name}}</a>
                                </div>
                            </li>
                        </ul>
                    </div>
        </div>
    </div>
</template>

<script>
import { Sketch } from '@ckpack/vue-color';

export default {
    name: 'EnrichmentLayerPane',
    props: ['active_termlayers','gephi_data','node_color_index',],
    emits: ['active_item_changed'],
    components: {
        Sketch
    },
    data() {
        return {
            hide: true,
            layer_item: {
                value: null,
                imageSrc: require('@/assets/pane/layer-icon.png')
            },
            terms: null,
            imageSrc: require('@/assets/pane/visible.png'),
            hiding_terms: new Set(),
            colorpalette: {},
            colors: 'rgba(0,0,0,1)',
            color_picker: false,
            term: null,
            mouseX: 0,
            mouseY: 0,
            intersectionSet: null,
            expand_proteins: true,
            expand_links: true,
            intersectingDicts: null
        }
    },
    watch: {
        active_termlayers: {
            handler(newList) {
            var com = this;

            if (newList == null) {
                com.terms = null
                return;
            }
            
            com.layer_item.value = newList

            this.colorpalette = this.$store.state.colorpalette

            com.terms  = newList.main

            com.intersectionSet = new Set();
            var intersectionSet = new Set();

            for (var checkElement of com.active_termlayers.main){
                if(!com.hiding_terms.has(checkElement) && com.active_termlayers.main.size >= 1){
                    intersectionSet= new Set(checkElement.proteins);
                    break
                }

            }
                
            for (var element of com.active_termlayers.main){
                if(!com.hiding_terms.has(element)){
                    intersectionSet = new Set(element.proteins.filter((value) => intersectionSet.has(value)));
                }

            }


            for (var proteins of this.gephi_data.nodes){
                if(intersectionSet.has(proteins.attributes["Ensembl ID"])){
                    com.intersectionSet.add(proteins)
                }
            }


            // Find intersecting dictionaries
            com.intersectingDicts = this.findIntersectingDictionaries(com.active_termlayers.main);
        

            

            com.$emit('active_item_changed',{ "layers": com.layer_item})
            

        },
        deep: true,
    },

    },
    methods: {
        select_enrichment(value){

            this.emitter.emit("searchEnrichment", value);
        },
        prehighlight(proteins){
            this.emitter.emit("highlightProteinList", proteins);
        },
        hide_termlayer(term){
            var com = this;

            if(com.hiding_terms.has(term)) com.hiding_terms.delete(term);
            else com.hiding_terms.add(term)

            this.emitter.emit("hideTermLayer", {"main": com.terms, "hide": com.hiding_terms});

        },
        handleColorChange(term) {
            var com = this;
            // Perform any desired actions or call other methods here
            // This method will be called whenever the color changes
            const colorObject = com.colors["rgba"]
            com.colorpalette[term.name] = `rgb(${colorObject.r},${colorObject.g},${colorObject.b})`;

            this.$store.commit('assign_colorpalette', com.colorPalette)

            this.emitter.emit("hideTermLayer", {"main": com.terms, "hide": com.hiding_terms});
            
        },
        open_picker(event,term){
            var com = this;

            const divElement = document.getElementById('layerpane');
            const rect = divElement.getBoundingClientRect();

            const x = rect.left;
            const y = rect.top;
            
            com.mouseX = event.clientX - x - 10;
            com.mouseY = event.clientY - y + 10;
            
            
            if(((com.term == term) && com.color_picker) || com.color_picker == false) { 
                
                com.term = term
                com.colors = this.colorpalette[term.name]
                com.color_picker = !com.color_picker 

            }else {
                com.term = term
                com.colors = this.colorpalette[term.name]
            }
            

        },
        show_layer(){
            var com = this;

            var selected_proteins = new Set()
            for (var checkElement of com.active_termlayers.main){
                if(!com.hiding_terms.has(checkElement) && com.active_termlayers.main.size >= 1){
                    selected_proteins = new Set([...selected_proteins, ...checkElement.proteins])
                }
                
            }

            if(com.hide){
                this.emitter.emit("hideSubset", selected_proteins);
            }
            else{
                this.emitter.emit("hideSubset", null);
            }
            com.hide = !com.hide
        },
        /**
        * Calling the procedure in component EnrichmentTool for enriching terms with given set.
        * @param {boolean} state - functional enrichment gets reverted or applied.
        */
        apply_func(state) {
            var com = this;

            var selected_proteins = new Set()
            for (var checkElement of com.active_termlayers.main){
                if(!com.hiding_terms.has(checkElement) && com.active_termlayers.main.size >= 1){
                    selected_proteins = new Set([...selected_proteins, ...checkElement.proteins])
                }
                
            }

            if (state) com.emitter.emit("enrichSubset", [...selected_proteins]);
            else com.emitter.emit("enrichSubset", null);
        },
        /**
        * Calling the procedure in component MainVis to highlight a specific node
        * @param {dict} value - A dictionary of a single node
        */
        select_node(value) {
            this.emitter.emit("searchNode", value);
        },
        copyclipboard(){
            var com = this;

            var textToCopy = [];
            for(var link of com.intersectionSet) textToCopy.push(link.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        findIntersectingDictionaries(mySet) {
            const result = [];
            const arr = Array.from(mySet);
            for (let i = 0; i < arr.length; i++) {
                for (let j = i + 1; j < arr.length; j++) {
                const dict1 = arr[i];
                const dict2 = arr[j];
                if (this.intersectingElements(dict1.proteins, dict2.proteins)) {
                    result.push([dict1, dict2]);
                }
                }
            }
            return result;
            },

            // Helper function to check if arrays have intersecting elements
            intersectingElements(arr1, arr2) {
            for (let i = 0; i < arr1.length; i++) {
                if (arr2.includes(arr1[i])) {
                return true;
                }
            }
            return false;
            }

    },
    
}
</script>

<style>

    .pane-show {
        transform: translateX(326px);
    }
    .color-rect {
        width: 20px;
        height: 20px;
        margin-right: 5px;
        position: relative;
        display: inline-flex;   
        border-radius: 5px;
        border-style: solid;
        border-width: 1px;
        border-color: white;
    }
    #hide-termlayer {
        width: 15px;
        height: 15px;
        margin-right: 5px;
        position: relative;
        border-radius: 15px;
        border-style: none;
        background-color: white;

    }
    #color-picker{
        position: absolute;
        z-index: 999;
    }
    .link-enrichment {
        font-size: 12px;
        text-align: left;
        height: 28%;
        overflow-y: scroll;
        margin-bottom: 20px;
    }

    .link-enrichment a {
	color: white;
	text-decoration: none;
    }

    #hide-termlayer.hide {
        background-color: black;
    }

    #highlighted_proteins {
        text-align: center;
        padding: 0 0 0 4px;
        font-size: 12px;
        overflow-y: scroll;
        height: 27%;
    }

</style>