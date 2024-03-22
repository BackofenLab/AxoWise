<template>
    <div id="route" class="context">
        <div class="search-field">
            <img class="search-field-icon" src="@/assets/toolbar/search.png">
            <input type="text" v-model="search_raw" class="empty" placeholder="enter context" @keyup.enter="search_context(search_raw)"/>
        </div>
        <div class="context-check">
            <span>rank by:</span>
            <div class="context-confirm">
                <span>citations</span>
                <input id="citation" type="checkbox" /><label for="citation"></label>
            </div>
            <div class="context-confirm">
                <span>year</span>
                <input id="year" type="checkbox" /><label for="year"></label>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'ContextSearch',
    props: ['active_node'],
    data() {
        return {
            search_raw:"",
            rank_year: false,
            rank_citations: false,
        }
    },
    mounted(){
    },
    watch:{
        active_node(){
            if (!this.active_node) {
                this.search_raw = ''
                this.path = false
            }
        }
    },
    methods:{
        search_context(context) {
            const [year, citations] = [document.getElementById('year').checked, document.getElementById('citation').checked];
            this.emitter.emit("searchContext", {"node":this.active_node ,"context": context, "rank": this.get_rank(year,citations)});
        },
        get_rank(year,citations) {
            return year && citations ? "all" : year ? "year" : citations ? "citations" : "all";
        }
    },
}
</script>

<style>
#route {
    color: white;
    font-family: 'ABeeZee', sans-serif;
    font-size: 0.7vw;
    width: 100%;
    height: 100%;
    padding: 2.3vw 1.3vw 0 1.3vw;
}

.context {
    background: rgba(222, 222, 222, 0.3);
}

.context .search-field{
    width: 80%;
    left: 65%;
    display: flex;
    background: #0A0A1A;
    transform: translateX(-70%);
    position: absolute;
    border-radius: 0;
    justify-content: center;
    z-index: 999;
}

#route .search-field input[type=text] {
    margin-left: 15%;
    font-size: 0.7vw;
    width: 83%;
    background: none;
    color: white;
    cursor: default;
    font-family: 'ABeeZee', sans-serif;
    border: none;
}

.context-check{
    margin-top: 2vw;
}

.context-confirm {
    font-family: 'ABeeZee', sans-serif;
    margin-left: 1vw;
    font-size: 0.7vw;
    display: flex;
}

.context-confirm [type="checkbox"] + label {
    display: block;
    cursor: pointer;
    font-family: sans-serif;
    font-size: 24px;
    line-height: 1.3;
    position: absolute;
    right: 30%;
    margin-top: 0.7%;
}

.context-confirm [type="checkbox"] + label:before {
    width: 1.2vw;
    height: 0.6vw;
    border-radius: 30px;
    background-color: #ddd;
    content: "";
    transition: background-color 0.5s linear;
    z-index: 5;
    position: absolute;
}
.context-confirm [type="checkbox"] + label:after {
    width: 0.4vw;
    height: 0.4vw;
    border-radius: 30px;
    background-color: #fff;
    content: "";
    transition: margin 0.1s linear;
    box-shadow: 0px 0px 5px #aaa;
    position: absolute;
    top: 10%;
    margin: 0.09vw 0 0 0.09vw;
    z-index: 10;
}

.context-confirm [type="checkbox"]:checked + label:after {
  margin: 0.09vw 0 0 0.69vw;
}

</style>