<template>
    <div class="text" v-if="active_termlayers !== null">
        <div class="headertext">
            <span>Term Visualization</span>
        </div>
        <div class="nodeattributes">
            <div class="p">
            <span>Layers:</span>
            </div>
            <div class="link" id="link">
                <ul>
                    <li class="membership" v-for="term in terms" :key="term" >
                        <div class="color-rect" @click="color_picker = !color_picker" :style="{ backgroundColor: colorpalette[term.name] }"></div>
                        <!-- <Sketch class="color-picker" v-if="color_picker==true" v-model="colors" @update:model-value="handleColorChange(term)"/> -->
                        <button class="hide-termlayer" @click="hide_termlayer(term)"></button>
                        <a href="#" v-on:click="select_enrichment(term)" @mouseenter="prehighlight(term.proteins)" @mouseleave="prehighlight(null)">{{term.name}}</a>
                    </li>
                </ul>
            </div>
            
        </div>
    </div>
</template>

<script>
// import { Sketch } from '@ckpack/vue-color';

export default {
    name: 'EnrichmentLayerPane',
    props: ['active_termlayers','gephi_data','node_color_index',],
    emits: ['active_item_changed'],
    components: {
        // Sketch
    },
    data() {
        return {
            layer_item: {
                value: null,
                imageSrc: require('@/assets/pane/layer-icon.png')
            },
            terms: null,
            hiding_terms: new Set(),
            colorpalette: {},
            colors: '#00cedf',
            color_picker: false
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
        handleColorChange() {
            // Perform any desired actions or call other methods here
            // This method will be called whenever the color changes
            console.log('Color changed!');
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
        position: relative;
        display: inline-flex;
    }
    .hide-termlayer {
        width: 20px;
        height: 20px;
        position: relative;
        border-radius: 20px;
        border-style: none;

    }
    .color-picker{
        position: absolute;
        z-index: 999;
    }

</style>