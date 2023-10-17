<template>
    <div class="tool-item">
        <div id="protein_highlight"  class="highlight_list">
                <div id="protein_highlight_header">
                    <div class="text">
                        <div class="headertext">
                            <span>Highlight Proteins</span>
                            <button v-on:click="unactive_proteinlist()" id="highlight-btn-min"></button>
                        </div>
                    </div>
                </div>
                <div class="highlight_main">
                    <textarea v-model="raw_text" rows="10" cols="30" autofocus></textarea>
                    <button v-on:click="highlight(raw_text)" id="highlight_protein">Go</button>
                </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'ProteinList',
    props: [''],
    emits: ['protein_active_changed'],
    data() {
        return {
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
        },
        unactive_proteinlist(){
            this.$emit("protein_active_changed", false);
        }
    },
    mounted(){
        var com = this;

        com.dragElement(document.getElementById("protein_highlight"));
    }
}
</script>