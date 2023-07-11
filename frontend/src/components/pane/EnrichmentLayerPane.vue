<template>
    <div class="text" v-if="active_termlayers !== null">
        <div class="headertext">
            <span>Term Visualization</span>
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
                    <Sketch id="color-picker" v-if="color_picker==true" v-model="colors" @update:model-value="handleColorChange(term)" :style="{ top: mouseY + 'px', left: mouseX + 'px' }" />
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
            mouseY: 0
        }
    },
    watch: {
        active_termlayers() {
            var com = this;
            
            if (com.active_termlayers == null) {
                com.terms = null
                return;
            }
            
            com.layer_item.value = com.active_termlayers

            this.colorpalette = this.$store.state.colorpalette

            com.terms  = com.active_termlayers.main


            com.$emit('active_item_changed',{ "layers": com.layer_item})
            

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

            
            com.mouseX = event.clientX - 10;
            com.mouseY = event.clientY + 10;
            
            
            if(((com.term == term) && com.color_picker) || com.color_picker == false) { 
                
                com.term = term
                com.colors = this.colorpalette[term.name]
                com.color_picker = !com.color_picker 

            }else {
                com.term = term
                com.colors = this.colorpalette[term.name]
            }
            

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
        position: fixed;
        z-index: 999;
    }
    .link-enrichment {
        font-size: 12px;
        text-align: left;
    }

    .link-enrichment a {
	color: white;
	text-decoration: none;
    }

    #hide-termlayer.hide {
        background-color: black;
    }

</style>