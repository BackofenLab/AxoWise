<template>
    <div class="pane" id="context-pane" v-show = "paneHidden == false">
        <div class="pane_header"  id="context-pane_header">
            <span>context search</span>
            <img  class="pane_close" src="@/assets/toolbar/cross.png" v-on:click="paneHidden = true">
        </div>
        <div class="context-sum-window" v-if="!summary_hidden">
            <div class="pane_header">
                <span>context summary</span>
                <img  class="pane_close" src="@/assets/toolbar/cross.png" v-on:click="summary_hidden = true">
            </div>
            <div class="context-text">
                <div class="text">{{ summary }}</div>
            </div>
        </div>
        <main class="leaderboard__profiles">
            <article class="leaderboard__profile" v-for="(entry, index) in context_results" :key="index" v-on:click="open_conclusion(entry.summary)">
            <span class="leaderboard__name">{{ index }}</span>
            <span class="leaderboard__value">{{ entry.pr }}<span>PR</span></span>
            </article>
            
        </main>

    </div>
</template>

<script>

export default {
    name:"ContextSection",
    data() {
        return{
            api: {
                context: "api/subgraph/context",
            },
            paneHidden:true,
            context_results: {"12312":{"summary":"dsfasfassdfasfasfasfasdfasdfasdfasdf","pr":23,"citations":324,"year":1235},
                              "12342":{"summary":"dfsdbbhmjmjhfmfhmfhjmfhjm","pr":2,"citations":324,"year":1235},
                              "54747":{"summary":"adfgadfavvv vfvavavadfvadfad","pr":223,"citations":324,"year":1235}},
            summary_hidden: true,
            summary: ""
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
        open_conclusion(summary){
            var com = this;
            com.summary_hidden = false;
            com.summary = summary

        },
        generateContext(base,context,rank){
            var com = this;
            com.paneHidden = false;

            this.getContext(base,context,rank)
        },
        getContext(base,context,rank){
            var com = this

            //Adding proteins and species to formdata 
            var formData = new FormData()
            formData.append('base', base)
            formData.append('context', context);
            formData.append('rank', rank);

            //POST request for generating pathways
            com.axios
            .post(com.api.context, formData)
            .then((response) => {
                // com.context_results = response.data.sort((t1, t2) => t1.pr - t2.pr)
                com.test = response.data
                console.log(response.data)
            })

        },
    },
    mounted(){
        this.dragElement(document.getElementById("context-pane"));

        this.emitter.on("searchContext",(state) => {
            this.generateContext(state.node.attributes["Name"], state.context, state.rank)
        })

        }
}
</script>



<style lang="scss">

    #context-pane {
        position: fixed;
        right: 1vw;
        top: 1vw;
        height: 60%;
        width: 12vw;
        display: block;
        background: #D9D9D9;
        backdrop-filter: blur(7.5px);
        -webkit-backdrop-filter: blur(7.5px);
        align-items: center;
        z-index: 99;
    }

    .context-sum-window{
        position: fixed;
        right: 14vw;
        top: 1vw;
        height: 20vw;
        width: 15vw;
        display: block;
        background: #D9D9D9;
        backdrop-filter: blur(7.5px);
        -webkit-backdrop-filter: blur(7.5px);
        align-items: center;
        z-index: 99;
    }

    .context-text {
        color: white;
        font-family: 'ABeeZee', sans-serif;
        font-size: 0.7vw;
        width: 100%;
        height: 100%;
        padding: 1.3vw 1.3vw 0 1.3vw;
    }

    .leaderboard {
    max-width: 490px;
    width: 100%;
    border-radius: 12px;
    
    
    &__profiles {
        padding: 1vw;
        display: grid;
        row-gap: 1vw;
    }
    
    &__profile {
        display: grid;
        grid-template-columns: 1fr 3fr 1fr;
        align-items: center;
        overflow: hidden;
        box-shadow: 0 5px 7px -1px rgba(51, 51, 51, 0.23);
        cursor: pointer;
        transition: transform 0.25s cubic-bezier(0.7, 0.98, 0.86, 0.98), box-shadow 0.25s cubic-bezier(0.7, 0.98, 0.86, 0.98);
        background-color: #fff;
        
        &:hover {
        transform: scale(1.1);
        box-shadow: 0 9px 47px 11px rgba(51, 51, 51, 0.18);
        }
    }
    
    &__name {
        color: #979cb0;
        font-weight: 600;
        font-size: 0.7vw;
        margin-left: 12px;
    }
    
    &__value {
        padding-left: 0.6vw;
        color: #0A0A1A;
        font-weight: 700;
        font-size: 2vw;
        text-align: right;
        
        & > span {
        opacity: .8;
        font-weight: 600;
        font-size: 0.7vw;
        margin-left: 0.5vw;
        }
    }
    }

    .leaderboard {
    box-shadow: 0 0 40px -10px rgba(0, 0, 0, .4);
    }
</style>