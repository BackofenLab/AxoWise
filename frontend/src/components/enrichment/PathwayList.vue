<template>
    <div id="pathways-list">
        <div class="tool-section-term">
            <div class="pathway-search">
                <img class="pathway-search-icon" src="@/assets/toolbar/search.png">
                <input type="text" v-model="search_raw" class="empty" placeholder="search pathway"/>
            </div>
            <div class="filter-section">
                <div id="pathway-filter" class="pre-full" v-on:click="handling_filter_menu()" :class="{ full: category_filtering == true }">
                    <span>{{ category }}</span>
                    <img  class="remove-filter" src="@/assets/pathwaybar/cross.png" v-on:click.stop="active_categories(null)" v-if="category !== 'Filter'">
                </div>
                <div id="list-filter-categories" v-show="category_filtering == true && terms !== null">
                        <div class="element" v-for="(entry, index) in filter_terms" :key="index" v-on:click="active_categories(entry.label);" :class="{ active_cat: active_categories_set.has(entry.label)}">
                            <a>{{ entry.label }}</a>
                        </div>
                </div>
            </div>
            <div class="function-section">
                <div id="function-filter" class="pre-full" @mouseover="functions_active = true" @mouseleave="functions_active = false" :class="{ full: category_filtering == true }">
                    <img class="bookmark-image" src="@/assets/toolbar/menu-burger.png" >
                </div>
                <div id="function-filter-categories" v-show="functions_active == true" @mouseover="functions_active = true" @mouseleave="functions_active = false">
                    <div class="bookmark-button" v-on:click="bookmark_off = !bookmark_off">
                        <img class="bookmark-image" src="@/assets/pathwaybar/favorite.png" :class="{recolor_filter: bookmark_off == false}">
                    </div>
                    <div class="export-button" v-on:click="export_enrichment()">
                        <img class="bookmark-image" src="@/assets/pathwaybar/csv.png">
                    </div> 
                </div>
            </div>
        </div>
        <div class="list-section">
            
            <div class="sorting">
                <a class="enrichment_filter" v-on:click="sort_alph = (sort_alph === 'asc') ? 'dsc' : 'asc'; sort_fdr = '' " >functional enrichment pathways ({{ filt_terms.size }})</a>
                <a class="fdr_filter" v-on:click="sort_fdr = (sort_fdr === 'asc') ? 'dsc' : 'asc'; sort_alph = '' " >fdr rate</a>
            </div>

            <div v-if="await_load == true" class="loading_pane" ></div>
            <div class="results" v-if="terms !== null && await_load == false" tabindex="0" @keydown="handleKeyDown" ref="resultsContainer">
                <table >
                    <tbody>
                        <tr v-for="(entry, index) in filt_terms" :key="index" class="option" :class="{ selected: selectedIndex === index }" v-on:click="select_term(entry,index)">
                            <td>
                                <div class="favourite-symbol">
                                <label class="custom-checkbox">
                                    <div class="checkbox-image" v-on:click.stop="add_enrichment(entry)" :class="{ checked: favourite_tab.has(entry)}" ref="checkboxStates"></div>
                                </label>
                                </div>
                            </td>
                            <td>
                                <div class="pathway-text">
                                    <a href="#" ref="selectedNodes">{{entry.name}}</a>
                                </div>
                            </td>
                            <td>
                                <a class="fdr-class">{{ entry.fdr_rate.toExponential(2) }}</a>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div v-if="terms.length == 0">
                <i>No terms available.</i>
                </div>
            </div>
        </div>

    </div>
</template>

<script>

export default {
    name: 'PathwayList',
    props: ['gephi_data','terms', 'await_load', 'filtered_terms','favourite_pathways'],
    data() {
        return{
            search_raw: "",
            filter_raw: "",
            sort_fdr: "",
            sort_alph: "",
            category: "Filter",
            active_categories_set: new Set(),
            category_filtering: false,
            filter_terms: [],
            bookmark_off: true,
            favourite_tab: new Set(),
            selectedIndex: -1,
            functions_active: false
        }
    },
    mounted(){
        this.emitter.on("bookmarkPathway", (value) => {
            this.add_enrichment(value)
        });
        this.emitter.on("visualizeLayer", () => {
            this.visualize_layers()
        });
        this.favourite_tab = new Set(this.favourite_pathways)
    },
    watch:{
        terms() {
            this.filter_options(this.terms)
        },
        
    },
    computed: {
        regex() {
            var com = this;
            return RegExp(com.search_raw.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
        },
        filt_terms() {
            var com = this;
            var filtered = com.terms;
            
            if (com.category != "Filter") {
            // If category is set, filter by category
            filtered = filtered.filter(function(term) {
                return  com.active_categories_set.has(term.category);
            });
            }

            if (com.search_raw !== "") {
            // If search term is not empty, filter by search term
            var regex = new RegExp(com.regex, 'i');
            filtered = filtered.filter(function(term) {
                return regex.test(term.name);
            });
            }

            if(com.sort_alph == "asc"){
                filtered.sort(function(t1, t2) { return (t1.name.toLowerCase() > t2.name.toLowerCase() ? 1 : (t1.name.toLowerCase() === t2.name.toLowerCase() ? 0 : -1)) })
            }else if(com.sort_alph == "dsc"){
                filtered.sort(function(t1, t2) { return (t2.name.toLowerCase() > t1.name.toLowerCase() ? 1 : (t1.name.toLowerCase() === t2.name.toLowerCase() ? 0 : -1)) })
            }

            if(com.sort_fdr == "asc"){
                filtered.sort((t1, t2) => t2.fdr_rate - t1.fdr_rate)
            }else if (com.sort_fdr == "dsc"){
                filtered.sort((t1, t2) => t1.fdr_rate - t2.fdr_rate)
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
        active_categories(category){

            if (!category) {
                this.reset_categories()
                return
            }
            if (this.active_categories_set.has(category)){
                if(this.active_categories_set.size == 1) {
                    this.reset_categories()
                    return
                }
                this.active_categories_set.delete(category)
            }else{
                this.active_categories_set.add(category)
            }
            this.category = [...this.active_categories_set].join(', ');
        },
        reset_categories() {
            this.category = "Filter";
            this.active_categories_set = new Set()
        },
        filter_options(terms) {
            var com = this
            com.filter_terms = []
            var remove_duplicates = [...new Set(terms.map(term => term.category))]
            remove_duplicates.forEach(term => {
                com.filter_terms.push({'label': term})
            })

        },
        select_term(term, index) {
            var com = this;
            this.selectedIndex = index
            com.emitter.emit("searchEnrichment", term);
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
        add_enrichment(enrichment) {
            if (!this.favourite_tab.has(enrichment)) {
                // Checkbox is checked, add its state to the object
                this.favourite_tab.add(enrichment)
            } else {
                // Checkbox is unchecked, remove its state from the object
                this.favourite_tab.delete(enrichment)
            }
            this.$emit("favourite_pathways_changed", this.favourite_tab);
        },
        visualize_layers(){
            var com = this;
            com.emitter.emit("hideTermLayer", {"main":com.favourite_tab, "hide": new Set()});
        },
        export_enrichment(){
            var com = this;

            //export terms as csv
            var csvTermsData = com.filt_terms;

            var terms_csv = 'category\tfdr_rate\tname\tgenes\n';

            csvTermsData.forEach(function(row) {
                terms_csv += row['category'] + '\t' + row['fdr_rate'] + '\t"'  + row['name'] + '"\t"' + row['symbols'] +'"';
                terms_csv += '\n';   
            });


            //Create html element to hidden download csv file
            var hiddenElement = document.createElement('a');
            hiddenElement.target = '_blank';
            hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(terms_csv);
            hiddenElement.download = 'Terms.csv';  
            hiddenElement.click();
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

            var container = document.getElementById('list-filter-categories');
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
    .pathways #pathways-list {
        width: 100%;
        height: 100%;
        z-index: 997;
        cursor: default;
        font-family: 'ABeeZee', sans-serif;

    }

    .pathwaybar-small #pathways-list {
        width: 99%;
        height: 96.92%;
        position: absolute;
        top:50%;
        transform: translateY(-50%);
        margin-left: 0.5%;
        border-radius: 5px;
        z-index: 997;
        cursor: default;
        font-family: 'ABeeZee', sans-serif;

    }

    .pathway-search {
        background: rgba(222, 222, 222, 0.3);
        padding: 0 0 0 0.3vw;
        height: 1.4vw;
        display: flex;
        align-items: center;
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
        margin-left: 0.5vw;
        width: 8vw;
        font-size: 0.85vw;
        background: none;
        color: white;
        cursor: default;
        border: none;
        font-family: 'ABeeZee', sans-serif;
    }

    .pathway-search [type="text"]::-webkit-input-placeholder {
    opacity: 70%;
    }
    
    .filter-section {
        background: rgba(222, 222, 222, 0.3);
        height: 1.4vw;
        width: 8vw;
        align-items: center;
        align-content: center;
        justify-content: center;
    }

    #pathway-filter {
        width: 100%;
        height: 100%;
        padding: 0.7vw;
        display: flex;
        align-items: center;
        justify-content: center;

    }

    #function-filter {
        width: 100%;
        height: 100%;
        padding: 0.5vw;
        display: flex;
        align-items: center;
        justify-content: center;

    }

    .pre-full{
        border-radius: 5px;
    }

    #pathway-filter span {
        display: block;
        width: 90%;
        font-size: 0.85vw;
        color: white;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        cursor: default;
        text-align: center;
        
    }

    #pathway-filter .remove-filter {
        width: 0.8vw;
        filter: invert(100%);
    }

    #pathway-filter-categories,
    #list-filter-categories {
        position: absolute;
        width: 8vw;
        max-height: 60%;
        padding: 0.3% 0 0.3% 0;
        -webkit-backdrop-filter: blur(7.5px);
        backdrop-filter: blur(7.5px);
        overflow-y: scroll;
        overflow-x: hidden;
        color: white;
        border-color: rgba(255, 255, 255, 30%);
        border-width: 1px;
        border-style: solid;
        z-index: 9999;
    
    }
    #function-filter-categories {
        position: absolute;
        width: 2vw;
        max-height: 60%;
        padding: 0.3% 0 0.3% 0;
        background: rgba(222, 222, 222, 0.3);
        -webkit-backdrop-filter: blur(7.5px);
        backdrop-filter: blur(7.5px);
        overflow-y: scroll;
        overflow-x: hidden;
        color: white;
        z-index: 999;
    
    }

    .function-section{

        background: rgba(222, 222, 222, 0.3);
        height: 1.4vw;
        width: 2vw;
        align-items: center;
        align-content: center;
        justify-content: center;
    }

    .list-section {
        width: 100%;
        height: 100%;
        position: absolute;
        padding: 0% 2% 2% 2%;
    }
    
    .visualize-button,
    .bookmark-button,
    .export-button {
        width: 100%;
        height: 3vw;
        padding: 0.5vw;
        display: flex;
        align-items: center;
        justify-content: center;
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
        height: 99%;
        overflow: scroll;
    }

    .option {
        display: -webkit-flex;
    }

    .sorting {
        font-size: 0.73vw;
        border-bottom: 1px solid;
        border-color: white;
        cursor: default;

    }

    #pathways-list .sorting,
    #pathways-set .sorting {
        margin-top: 0.1vw;
        margin-left: 1vw;
        padding-bottom: 0.1vw;
        width: 90%;
    }

    .sorting a {
        color: rgba(255, 255, 255, 0.7);
    }

    .fdr_filter{
        position: absolute;
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
        -webkit-filter: invert(100%); 
        filter: invert(100%);
    }

    .visualize-logo {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;

    }
    /* .visualize-logo .bookmark-image {
    } */
    .visualize-text {
        font-size: 0.95vw;
        color: white;
        
    }

    .recolor_filter {
        filter: invert(71%) sepia(19%) saturate(7427%) hue-rotate(360deg) brightness(104%) contrast(105%);
    }

    /* Hide scrollbar for Chrome, Safari and Opera */
    #pathway-filter-categories::-webkit-scrollbar,
    #home-filter-categories::-webkit-scrollbar 
    #list-filter-categories::-webkit-scrollbar {
        display: none;
    }

    /* Hide scrollbar for IE, Edge and Firefox */
    #pathway-filter-categories,
    #home-filter-categories, 
    #list-filter-categories {
        -ms-overflow-style: none;  /* IE and Edge */
        scrollbar-width: none;  /* Firefox */
    }

    #pathway-filter-categories .element,
    #home-filter-categories .element,
    #list-filter-categories .element{
        position: relative;
        padding: 5%;
        flex-shrink: 0;
        border-top-color: rgba(255, 255, 255, 30%);
        border-top-width: 1px;
        border-top-style: solid;
        transform-origin: center center;
        transform: scale(1);
        scroll-snap-align: center;
        display: flex;
    }

    .element a {
        width: 100%;
        color: white;
        padding: 5%;
        font-size: 0.6vw;
        align-self: center;
        text-align: center;
    }

    #pathway-filter-categories .active_cat,
    #home-filter-categories .active_cat,
    #list-filter-categories .active_cat {
        background: #ffa500;
    }


</style>