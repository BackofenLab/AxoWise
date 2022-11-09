Vue.component("protein_list", {
    props: ["gephi_json","protein_list"],
    data: function() {
        return  {
            status: "",
            raw_text: "",
            proteins: null,
        }
    },
    methods: {
        dragElement: function(elmnt) {

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
        highlight: function(){
            var com = this;
            com.proteins = com.raw_text.toLowerCase().split("\n");
            
            var subset = [];
            var proteins_set = new Set(com.proteins);
            sigma_instance.graph.nodes().forEach(function (n) {
                if (proteins_set.has(n.label.toLowerCase())){
                    subset.push(n);
                }
            });

            com.$emit("active-subset-changed", subset);

        },
        hide: function(){
            var com = this;

            com.$emit("protein-list-changed", "HIDE");

        },
            
    },
    watch: {
        "protein_list": function(status) {
            var com = this;

            com.status=status;

        },
    },
    mounted: function(){
        var com = this;

        com.dragElement(document.getElementById("protein_highlight"));

    },
    template: `
        <div id="protein_highlight" v-show="status === 'SHOW'" class="highlight_list">
                <div id="protein_highlight_header">
                        <div class="text">
                            <div class="headertext">
                                <span>Highlight Proteins</span>
                                <button v-on:click="hide()" id="highlight-btn-min"></button>
                            </div>
                        </div>
                </div>
                <div class="highlight_main">
                    <textarea v-model="raw_text" rows="10" cols="30" autofocus></textarea>
                    <button v-on:click="highlight()" id="highlight_protein">Go</button>
                </div>
        </div>
    `
});