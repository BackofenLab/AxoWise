<template>
    <div id="pathway-layer-show">
        <div class="pane-sorting">
            <a class="pane_values">term</a>
        </div>

        <div class="network-results" tabindex="0" @keydown="handleKeyDown">
            <table >
                <tbody>
                    <tr v-for="(entry) in terms" :key="entry" class="option">
                        <td>
                            <div class="statistics-attr">
                                <div class="color-rect" id="color_rect" @click="open_picker($event,entry);" :style="{ backgroundColor: colorpalette[entry.name] }"></div>
                            </div>
                        </td>
                        <td>
                            <div class="statistics-hide">
                                <img src="@/assets/pane/invisible.png" @click="hide_termlayer(entry)" v-if="hiding_terms.has(entry)">
                                <img src="@/assets/pane/visible.png" @click="hide_termlayer(entry)" v-if="!hiding_terms.has(entry)">
                            </div>
                        </td>
                        <td>
                            <div class="statistics-val">
                                <a href="#">{{entry.name}}</a>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div id="pathway_color" class="color-picker-sketch" v-show="color_picker==true">
        <div id="pathway_color_header" class="window-header">
                <div class="headertext">
                    <span>coloring menu</span>
                    <img  class="protein_close" src="@/assets/pathwaybar/cross.png" v-on:click="color_picker=false">
                </div>
        </div>
            <Sketch id="color-picker" v-model="colors" @update:model-value="handleColorChange(term)" :style="{ top: mouseY + 'px', left: mouseX + 'px' }" />
        </div>
    </div>
</template>

<script>
import { Sketch } from '@ckpack/vue-color';

export default {
    name: 'PathwayLayers',
    props: ['active_termlayers','gephi_data','hiding_terms_changed'],
    components: {
        Sketch
    },
    data() {
        return {
            terms: null,
            colorpalette: null,
            hiding_terms: new Set(),
            color_picker: false,
            colors: 'rgba(0,0,0,1)',
            mouseX: 0,
            mouseY: 0,
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

            this.colorpalette = this.$store.state.colorpalette
            com.terms  = newList.main
            },
        deep: true,
        },
    },
    methods: {
        handleColorChange(term) {
            var com = this;

            const colorObject = com.colors["rgba"]
            com.colorpalette[term.name] = `rgb(${colorObject.r},${colorObject.g},${colorObject.b})`;

            this.$store.commit('assign_colorpalette', com.colorPalette)

            this.emitter.emit("hideTermLayer", {"main": com.terms, "hide": com.hiding_terms});
            
        },
        open_picker(event,term){
            var com = this;

            
            com.color_picker = true
            if(com.color_picker) this.dragElement(document.getElementById("pathway_color"));
            com.term = term
            com.colors = this.colorpalette[term.name]
            
        },
        hide_termlayer(term){
            var com = this;

            if(com.hiding_terms.has(term)) com.hiding_terms.delete(term);
            else com.hiding_terms.add(term)

            com.$emit('hiding_terms_changed',com.hiding_terms)
            this.emitter.emit("hideTermLayer", {"main": com.terms, "hide": com.hiding_terms});

        },
        select_enrichment(value){
         this.emitter.emit("searchEnrichment", value);
        },
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
                // calculate the new cursor position:
                pos1 = pos3 - e.clientX;
                pos2 = pos4 - e.clientY;
                pos3 = e.clientX;
                pos4 = e.clientY;
                // set the element's new position:
                elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
                elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
            }

            function closeDragElement() {
                // stop moving when mouse button is released:
                document.onmouseup = null;
                document.onmousemove = null;
            }
        }
    },
}
</script>

<style>
#pathway-layer-show {
    width: 100%;
    height: 100%;
    top: 9.35%;
    position: absolute;
    font-family: 'ABeeZee', sans-serif;
    padding: 0% 2% 2% 2%;
}
#pathway-layer-show .network-results {
    margin-top: 2%;
    height: 82%;
    overflow: scroll;
}
#pathway-layer-show .color-rect {
    width: 0.7vw;
    height: 0.7vw;
    margin-right: 5px;
    position: relative;
    display: inline-flex;   
    border-radius: 5px;
    border-style: solid;
    border-width: 1px;
    border-color: white;
}
#pathway-layer-show .network-results td:first-child {
    width: 8%;
    align-self: center;
}
#pathway-layer-show .network-results td:nth-child(2) {
    font-size: 0.7vw;
    margin-bottom: 1%;
    color: white;
    width:  10%;
    align-self: center;
    white-space: nowrap;
    overflow: hidden;    /* Hide overflow content */
    text-overflow: ellipsis;
}
#pathway-layer-show .network-results td:last-child {
    font-size: 0.7vw;
    margin-bottom: 1%;
    color: white;
    width:  90%;
    align-self: center;
    white-space: nowrap;
    overflow: hidden;    /* Hide overflow content */
    text-overflow: ellipsis;
}
#pathway-layer-show .statistics-attr{
    margin-left: 25%;
}
#pathway-layer-show .statistics-val{
    display: flex;
    height: 1vw;
    width: 80%;
    white-space: nowrap;
    overflow: hidden;    /* Hide overflow content */
    text-overflow: ellipsis;
}
#pathway-layer-show .statistics-val a {
    cursor: default;
    font-size: 0.7vw;
    color: white;
    text-decoration:none;
}
#pathway-layer-show .pane_values{
    position: relative;
    left: 0%;
}
#pathway-layer-show .statistics-hide{
    display: -webkit-flex;
}
#pathway-layer-show .statistics-hide img {
    padding: 5% 25% 5% 25%;
    filter: invert(100%);
}
#color-picker{
    margin-top: 5%;
    position: absolute;
    z-index: 1001;
    width: -webkit-fill-available;
    background: rgba(222, 222, 222, 0.61);
}
.color-picker-sketch{
    display: flex;
    position: fixed;
    top: 30%;
    width: 15%;
    right: 38%;
    z-index: 1000;
}
#pathway_color_header{
    position: relative;
    z-index: 1002;
}
</style>