<template>
    <div class="tool-item">
        <div id="protein_highlight">
            <div class="highlight_list">
                    <textarea v-model="raw_text" rows="10" cols="30" autofocus></textarea>
                    <button v-on:click="highlight(raw_text)" id="highlight_protein">search</button>
            </div>  
            <div id="protein_highlight_header">
                <div class="headertext">
                    <span>highlight proteins</span>
                    <img  class="protein_close" src="@/assets/pathwaybar/cross.png" v-on:click="unactive_proteinlist()">
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'ProteinList',
    emits: ['protein_active_changed'],
    data() {
        return {
            raw_text: "",
            protein_data: this.$store.state.gephi_json.data,
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
        },
        highlight(proteins) {
            var com = this

            const protein_names = new Set(proteins.toUpperCase().split("\n"))
            const subset = []
            com.protein_data.nodes.forEach(node => {
                if(protein_names.has(node.attributes['Name'])){
                    subset.push(node)
                }
            });

            com.emitter.emit("searchSubset", subset);
        },
    },
    mounted(){
        var com = this;

        com.dragElement(document.getElementById("protein_highlight"));
    }
}
</script>

<style>

#protein_highlight {
    position: fixed;
    top: 30%;
    left: 42%;
    width: 16%;
    height: 30%;
    flex-shrink: 0;

}
.highlight_list {
    position: absolute;
    top: 9.41%;
    width: 100%;
    height: 80%;
    border-radius: 0px 0px 5px 5px;
    background: rgba(222, 222, 222, 0.61);
    backdrop-filter: blur(7.5px);
    text-align: center;
}

#protein_highlight_header {
    width: 100%;
    height: 9.41%;
    position: absolute;
    flex-shrink: 0;
    border-radius: 5px 5px 0px 0px;
    backdrop-filter: blur(7.5px);
    background: #D9D9D9;
    text-align: center;
}

#protein_highlight_header .headertext{
	color:  #0A0A1A;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}
#protein_highlight_header .headertext span{
    height: 100%;
    display: flex;
    font-size: 0.9vw;
    align-items: center;
}

#protein_highlight_header .protein_close{
    right: 3%;
    width: 0.9vw;
    height: 0.9vw;
    filter: invert(100%);
    position: absolute;
}

.highlight_list textarea {
    margin-top: 5%;
	border-radius: 5px;
	font-size: 0.9vw;
    width: 90%;
	color: white;
	background-color:  rgba(10, 10, 26, 0.5);
	text-align: center;
	border: none;
	padding-top: 5%;
	resize: none;
	outline: none;
	height: 80%;
}

#highlight_protein {
	position: absolute;
	display: block;
	background-color:#0A0A1A;
	cursor: pointer;
    border: none;
	color: white;
	border-radius: 5px;
	padding: 1%;
	width: 60%;
	margin-left: 50%;
	margin-top: 1%;
	transform: translate(-50%,0);
}

</style>