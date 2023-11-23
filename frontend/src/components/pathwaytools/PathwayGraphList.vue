<template>
    <div id="pathways-list">
        <div class="pathway-search">
            <img class="pathway-search-icon" src="@/assets/toolbar/search.png">
            <input type="text" v-model="search_raw" class="empty" placeholder="Find your pathways"/>
        </div>
        <div id="pathway-filter" v-on:click="handling_filter_menu()" >
            <span>{{ category }}</span>
            <img  class="remove-filter" src="@/assets/pathwaybar/cross.png" v-on:click.stop="category = 'Filter'" v-if="category !== 'Filter'">
        </div>
        <div id="pathway-filter-categories" v-show="category_filtering == true && term_data !== null">
            <div class="element" v-for="(entry, index) in filter_terms" :key="index" v-on:click="category = entry.label; handling_filter_menu()">
                <a>{{ entry.label }}</a>
            </div>
        </div>
        <div class="list-section">
            
            <div class="sorting">
                <a class="enrichment_filter" v-on:click="sort_alph = (sort_alph === 'asc') ? 'dsc' : 'asc'; sort_fdr = '' " >functional enrichment pathways ({{ filt_terms.size }})</a>
                <a class="fdr_filter" v-on:click="sort_fdr = (sort_fdr === 'asc') ? 'dsc' : 'asc'; sort_alph = '' " >fdr rate</a>
            </div>

            <div class="results" v-if="term_data !== null" tabindex="0" @keydown="handleKeyDown" ref="resultsContainer">
                <table >
                    <tbody>
                        <tr v-for="(entry, index) in filt_terms" :key="index" class="option" :class="{ selected: selectedIndex === index }" v-on:click="select_term(entry,index)">
                            <td></td>
                            <td>
                                <div class="pathway-text">
                                    <a href="#" ref="selectedNodes">{{entry.attributes["Name"]}}</a>
                                </div>
                            </td>
                            <td>
                                <a class="fdr-class">{{ entry.attributes["FDR"].toExponential(2) }}</a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

    </div>
</template>

<script>

export default {
    name: 'PathwayGraphList',
    props: ['term_data','terms', 'filtered_terms'],
    data() {
        return{
            search_raw: "",
            filter_raw: "",
            sort_fdr: "",
            sort_alph: "",
            category: "Filter",
            category_filtering: false,
            filter_terms: [],
            bookmark_off: true,
            favourite_tab: new Set(),
            selectedIndex: -1,
            mode: 'term'
        }
    },
    mounted(){
        this.filter_options(this.term_data.nodes)
    },
    computed: {
        regex() {
            var com = this;
            return RegExp(com.search_raw.toLowerCase());
        },
        filt_terms() {
            var com = this;
            var filtered = com.term_data.nodes;

            console.log(filtered)
            
            if (com.category != "Filter") {
            // If category is set, filter by category
            filtered = filtered.filter(function(term) {
                return term.attributes["Category"] === com.category;
            });
            }

            if (com.search_raw !== "") {
            // If search term is not empty, filter by search term
            var regex = new RegExp(com.regex, 'i');
            filtered = filtered.filter(function(term) {
                return regex.test(term.attributes["Name"]);
            });
            }

            if(com.sort_alph == "asc"){
                filtered.sort(function(t1, t2) { 
                    return (t1.attributes["Name"].toLowerCase() > t2.attributes["Name"].toLowerCase() ? 1 : (t1.attributes["Name"].toLowerCase() === t2.attributes["Name"].toLowerCase() ? 0 : -1)) })
            }else if(com.sort_alph == "dsc"){
                filtered.sort(function(t1, t2) { 
                    return (t2.attributes["Name"].toLowerCase() > t1.attributes["Name"].toLowerCase() ? 1 : (t1.attributes["Name"].toLowerCase() === t2.attributes["Name"].toLowerCase() ? 0 : -1)) })
            }

            if(com.sort_fdr == "asc"){
                filtered.sort((t1, t2) => t2.attributes["FDR"] - t1.attributes["FDR"])
            }else if (com.sort_fdr == "dsc"){
                filtered.sort((t1, t2) => t1.attributes["FDR"] - t2.attributes["FDR"])
            }

            if (!com.bookmark_off){
                filtered = filtered.filter(function(term) {
                    return com.favourite_tab.has(term)
                });
            }

            this.$emit('filtered_terms_changed', filtered)
            return new Set(filtered);
        },
    },
    methods: {
        filter_options(terms) {
            var com = this
            com.filter_terms = []
            var remove_duplicates = [...new Set(terms.map(term => term.attributes["Category"]))]
            remove_duplicates.forEach(term => {
                com.filter_terms.push({'label': term})
            })

            console.log(com.filter_terms)
        },
        select_term(term, index) {
            var com = this;
            this.selectedIndex = index
            com.emitter.emit("searchNode", {'node': term, 'mode': this.mode});
        },
        scrollToSelected(selectedDiv) {
            const parent = this.$refs.resultsContainer; // Updated line to use this.$refs

            if (!selectedDiv) {
                return;
            }

            const selectedDivPosition = selectedDiv.getBoundingClientRect()
            const parentBorders = parent.getBoundingClientRect()

            if(selectedDivPosition.bottom >= parentBorders.bottom){
                selectedDiv.scrollIntoView(false);
            }

            if(selectedDivPosition.top <= parentBorders.top){
                selectedDiv.scrollIntoView(true);
            }

        },
        handleKeyDown(event) {
            const keyCode = event.keyCode;

            if (keyCode === 38) {
                event.preventDefault();
                if (this.selectedIndex > 0){
                    this.selectedIndex--;
                    this.scrollToSelected(this.$refs.selectedNodes[this.selectedIndex])
                    this.clickNode()
                }
            } else if (keyCode === 40) {
                event.preventDefault();
                if (this.selectedIndex < this.filt_terms.size - 1){
                    this.selectedIndex++;
                    this.scrollToSelected(this.$refs.selectedNodes[this.selectedIndex])
                    this.clickNode()
                }
            }
        },
        clickNode() {
            const selectedNode = this.$refs.selectedNodes[this.selectedIndex];
            if (selectedNode) {
                selectedNode.click();
            }
        },
        handling_filter_menu() {
            var com = this;
            if (!com.category_filtering) {
                com.category_filtering = true;

                // Add the event listener
                document.addEventListener('mouseup', com.handleMouseUp);
            }
            else{
                com.category_filtering = false;
                document.removeEventListener('mouseup', com.handleMouseUp);
            }

        },
        handleMouseUp(e) {
            var com = this;

            var container = document.getElementById('pathway-filter-categories');
            var container_button = document.getElementById('pathway-filter');
            if (!container.contains(e.target) && !container_button.contains(e.target)) {
                com.category_filtering = false;

                // Remove the event listener
                document.removeEventListener('mouseup', com.handleMouseUp);
            }
        }
    }, 
}
</script>


<style>
    #pathways-list {
        width: 32.83%;
        height: 96.92%;
        position: absolute;
        top:50%;
        transform: translateY(-50%);
        margin-left: 0.28%;
        border-radius: 5px;
        z-index: 997;
        cursor: default;
        font-family: 'ABeeZee', sans-serif;

    }

    .pathway-search {
        width: 37.54%;
        height: 11.16%;
        display: flex;
        position: absolute;
        align-items: center;
        border-radius: 5px;
        background: #0A0A1A;
        align-content: center;
        justify-content: center;
    }
    
    .pathway-search-icon {
        margin-left: 3%;
        position: relative;
        height: 0.9vw;
        width: 0.9vw;
        filter: invert(100%);
    }

    .pathway-search input[type=text] {
        margin-left: 2%;
        font-size: 0.85vw;
        width: 80%;
        background: none;
        color: white;
        cursor: default;
        font-family: 'ABeeZee', sans-serif;
    }

    .pathway-search [type="text"]::-webkit-input-placeholder {
    opacity: 70%;
    }

    #pathway-filter {
        width: 17.81%;
        left: 38.54%;
        height: 11.16%;
        display: flex;
        position: absolute;
        border-radius: 5px;
        background: #0A0A1A;
        align-items: center;
        justify-content: center;
    }

    #pathway-filter span {
        display: block;
        width: 90%;
        font-size: 0.95vw;
        color: white;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        cursor: default;
        text-align: center;
    }

    #pathway-filter .remove-filter {
        width: 10%;
        padding: 0%;
        filter: invert(100%);
        position: absolute;
        top: 6%;
        right: 4%;
        padding-top: 1%;
        filter: invert(100%);
    }

    #pathway-filter-categories {
        display: flex;
        position: fixed;
        width: 92.05%;
        height: 30.32%;
        left: 20%;
        top: 15%;
        padding: 1% 0.5% 1% 0.5%;
        border-radius: 5px;
        border: 1px solid #FFF;
        background: #0A0A1A;
        z-index: 1;
        align-items: center;
        overflow-x: scroll;
        overflow-y: hidden;
        cursor: default;
    }

    #pathway-filter-categories .element {
        border-radius: 5px;
        background: rgba(217, 217, 217, 0.17);
        display: flex;
        width: 26.88%;
        height: 100%;
        margin: 0% 1% 0% 1%;
        overflow: hidden;

    }
    #pathway-filter-categories .element:hover {
        background: rgba(217, 217, 217, 0.47);
    }
    .element a {
        width: 100%;
        color: white;
        padding: 5%;
        font-weight: bold;
        font-size: 0.4vw;
        align-self: center;
        text-align: center;
    }


    .list-section {
        width: 100%;
        height: 87.65%;
        top: 12.35%;
        border-radius: 5px;
        background: #0A0A1A;
        position: absolute;
        padding: 0% 2% 2% 2%;
    }
    .bookmark-button {
        width: 7.51%;
        height: 11.16%;
        left: 57.35%;
        position: absolute;
        border-radius: 5px;
        background: #0A0A1A;
        align-content: center;
        justify-content: center;
    }
    .visualize-button {
        width: 17.24%;
        height: 11.16%;
        left: 65.86%;
        position: absolute;
        border-radius: 5px;
        background: #0A0A1A;
        text-align: center;
        cursor:default;
    }
    .export-button {
        width: 15.8%;
        height: 11.16%;
        left: 84.1%;
        position: absolute;
        border-radius: 5px;
        background: #0A0A1A;
        cursor: default;

    }

    .export-button .export-text {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.95vw;
    }

    .list-section a {
        color: white;
        text-decoration:none;
    }

    .list-section .results {
        height: 90%;
        overflow: scroll;
    }

    .option {
        display: -webkit-flex;
    }

    .sorting {
        margin-top: 0.1vw;
        margin-left: 1.35vw;
        padding-bottom: 0.1vw;
        width: 91%;
        font-size: 0.73vw;
        border-bottom: 1px solid;
        border-color: white;
        cursor: default;

    }
    .sorting a {
        color: rgba(255, 255, 255, 0.7);
    }

    .fdr_filter{
        position: fixed;
        left: 78.6%;
    }

    .pathway-text{
        width: 92%;
        white-space: nowrap;
        overflow: hidden;    /* Hide overflow content */
        text-overflow: ellipsis;
        margin-left: 2%;
    }

    .pathway-text a {
        cursor: default;
    }

    /* bookmark styles */

    table {
        display: flex;
        width: 100%;
    }

    :focus {outline:0 !important;}

    table tbody{
        width: 100%;
    }
    td:first-child {
    width: 3.41%;
    align-self: center;
    }
    td:nth-child(2) {
    color: #FFF;
    font-size: 0.9vw;
    width: 91.55%;
    overflow: hidden;
    align-self: center;
    }
    td:last-child {
    font-size: 0.9vw;
    color: white;
    width:  24.04%;
    align-self: center;
    }

    .favourite-symbol{
        width: 100%;
        height: 100%;
        justify-content: center;
        text-align: center;
        position: relative;
        display: flex;
        
    }
    .custom-checkbox {
        position: relative;
        display: inline-block;
        cursor: default;
    }

    .checkbox-image {
        display: block;
        width: 0.9vw;
        height: 0.9vw;
        background-color: white;
        -webkit-mask: url(@/assets/pathwaybar/star-solid.svg) no-repeat center;
        mask: url(@/assets/pathwaybar/star-solid.svg) no-repeat center;
        mask-size: 0.9vw;
        background-repeat: no-repeat;
    }

    .checked {
        background-color: #ffa500;
    }

    .selected {
        background-color: rgba(255,0,0,0.7);
    }

    .bookmark-image {
        width: 100%;
        height: 100%;
        padding: 5% 23% 5% 23%;
        -webkit-filter: invert(100%); /* Safari/Chrome */
        filter: invert(100%);
    }

    .visualize-logo {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;

    }
    .visualize-logo .bookmark-image {
        margin-left: 3%;
        width: 25%;
        height: 85%;
        padding: 0%;
        filter: invert(100%);
        padding-top:1%;
    }
    .visualize-text {
        font-size: 0.95vw;
        color: white;
        
    }

    .recolor_filter {
        filter: invert(71%) sepia(19%) saturate(7427%) hue-rotate(360deg) brightness(104%) contrast(105%);
    }


</style>