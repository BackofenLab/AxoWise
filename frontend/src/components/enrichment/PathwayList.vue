<template>
    <div id="pathways-list">
        <div class="pathway-search">
            <img class="pathway-search-icon" src="@/assets/toolbar/search.png">
            <input type="text" v-model="search_raw" class="empty" placeholder="Find your pathways"/>
        </div>
        <div class="pathway-filter" v-on:click="category_filtering = !category_filtering">
            <span>{{ category }}</span>
            <img  class="remove-filter" src="@/assets/pathwaybar/cross.png" v-on:click.stop="category = 'Filter'" v-if="category !== 'Filter'">
        </div>
        <div class="pathway-filter-categories" v-if="category_filtering == true && terms !== null">
            <div class="element" v-for="(entry, index) in filter_terms" :key="index" v-on:click="category = entry.label; category_filtering = false">
                <a>{{ entry.label }}</a>
            </div>
        </div>
        <div class="bookmark-button" v-on:click="bookmark_off = !bookmark_off">
            <img class="bookmark-image" src="@/assets/pathwaybar/favorite.png" :class="{recolor_filter: bookmark_off == false}">
        </div>
        <div class="visualize-button" v-on:click="visualize_layers()">
            <div class="visualize-logo">
                <span class="visualize-text">Layers</span>
                <img class="bookmark-image" src="@/assets/pathwaybar/favorite.png">
            </div>
        </div>
        <div class="export-button" v-on:click="export_enrichment()">
            <div class="export-text">Export</div>
        </div>
        <div class="list-section">
            
            <div class="sorting">
                <a class="enrichment_filter" v-on:click="sort_alph = (sort_alph === 'asc') ? 'dsc' : 'asc'; sort_fdr = '' " >functional enrichment pathways</a>
                <a class="fdr_filter" v-on:click="sort_fdr = (sort_fdr === 'asc') ? 'dsc' : 'asc'; sort_alph = '' " >fdr rate</a>
            </div>

            <div v-if="await_load == true" class="loading_pane" ></div>
            <div class="results" v-if="terms !== null && await_load == false" tabindex="0" @keydown="handleKeyDown" ref="resultsContainer">
                <table >
                    <tbody>
                        <tr v-for="(entry, index) in filt_terms" :key="index" class="option" :class="{ selected: selectedIndex === index }">
                            <td>
                                <div class="favourite-symbol">
                                <label class="custom-checkbox">
                                    <div class="checkbox-image" v-on:click="add_enrichment(entry)" :class="{ checked: favourite_tab.has(entry)}" ref="checkboxStates"></div>
                                </label>
                                </div>
                            </td>
                            <td>
                                <div class="pathway-text" v-on:click="select_term(entry,index)">
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
    props: ['gephi_data','active_term'],
    data() {
        return{
            api: {
                subgraph: "api/subgraph/enrichment",
            },
            terms: null,
            await_load: false,
            search_raw: "",
            filter_raw: "",
            bookmark_off: true,
            selectedIndex: -1,
            sort_fdr: "",
            sort_alph: "",
            category: "Filter",
            favourite_tab: new Set(),
            category_filtering: false,
            filter_terms: []
        }
    },
    mounted() {
        var com = this
        com.generatePathways(com.gephi_data.nodes[0].species, com.gephi_data.nodes.map(node => node.id))


    },
    watch: {
        terms() {
            this.filtered_terms = this.terms
        },
    },
    computed: {
        regex() {
            var com = this;
            return RegExp(com.search_raw.toLowerCase());
        },
        filt_terms() {
            var com = this;
            var filtered = com.terms;
            
            if (com.category != "Filter") {
            // If category is set, filter by category
            filtered = filtered.filter(function(term) {
                return term.category === com.category;
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
            

            return new Set(filtered);
        },
    },
    methods: {
        generatePathways(species, proteins){
            var com = this

            //Adding proteins and species to formdata 
            var formData = new FormData()
            formData.append('proteins', proteins)
            formData.append('species_id', species);
                
            //POST request for generating pathways
            com.axios
            .post(com.api.subgraph, formData)
            .then((response) => {
                com.$store.commit('assign_enrichment', response.data.sort((t1, t2) => t1.fdr_rate - t2.fdr_rate))
                com.terms = com.$store.state.enrichment_terms
                // com.get_term_data(formData)
                com.filter_options()
                com.await_load = false
            })

        },
        filter_options() {
            var com = this
            com.filter_terms = []
            var remove_duplicates = [...new Set(com.terms.map(term => term.category))]
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
        },
        visualize_layers(){
            var com = this;
            com.emitter.emit("hideTermLayer", {"main":com.favourite_tab, "hide": new Set()});
        },
        export_enrichment(){
            var com = this;

            //export terms as csv
            var csvTermsData = com.filt_terms;

            var terms_csv = 'category\tfdr_rate\tname\tproteins\n';
            
            // Create a mapping between Ensembl ID and label
            const ensemblIdToLabelMap = {};
            for (const node of com.gephi_data.nodes) {
            ensemblIdToLabelMap[node.attributes["Ensembl ID"]] = node.label;
            }

            csvTermsData.forEach(function(row) {
                var protein_names = []
                for (const ensemblId of row['proteins']) {
                    const label = ensemblIdToLabelMap[ensemblId];
                    if (label) {
                        protein_names.push(label);
                    }
                
                }
                terms_csv += row['category'] + '\t' + row['fdr_rate'] + '\t"'  + row['name'] + '"\t"' +protein_names+'"';
                terms_csv += '\n';   
            });


            //Create html element to hidden download csv file
            var hiddenElement = document.createElement('a');
            hiddenElement.target = '_blank';
            hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(terms_csv);
            hiddenElement.download = 'Terms.csv';  
            hiddenElement.click();
        },
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
        border-radius: 10px;
        z-index: 999;

    }

    .pathway-search {
        width: 37.54%;
        height: 11.16%;
        display: flex;
        position: absolute;
        align-items: center;
        background-image: url(@/assets/pathwaybar/pathway-button.png);
        background-size: 100% 100%;
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
        font-size: 0.9vw;
        width: 80%;
        background: none;
        color: white;
    }

    .pathway-search [type="text"]::-webkit-input-placeholder {
    opacity: 50%; /* Make input background transparent */
    }

    .pathway-filter {
        width: 20.54%;
        left: 35.7%;
        height: 11.16%;
        display: flex;
        position: absolute;
        align-items: center;
        background-image: url(@/assets/pathwaybar/pathway-button-2.png);
        background-size: 100% 100%;
    }

    .pathway-filter span {
        display: block;
        width: 60%;
        margin-left: 30%;
        padding-bottom: 2%;
        font-size: 0.9vw;
        color: white;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        cursor: default;
    }

    .pathway-filter .remove-filter {
        width: 10%;
        padding: 0%;
        filter: invert(100%);
        position: absolute;
        top: 6%;
        right: 4%;
        padding-top: 1%;
        filter: invert(100%);
    }

    .pathway-filter-categories {
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

    .pathway-filter-categories .element {
        border-radius: 5px;
        background: rgba(217, 217, 217, 0.17);
        display: flex;
        width: 26.88%;
        height: 100%;
        margin: 0% 1% 0% 1%;
        overflow: hidden;

    }
    .pathway-filter-categories .element:hover {
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
        border-radius: 10px;
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
        padding-bottom: 2%;
        color: white;
        font-size: 0.9vw;
    }

    .list-section a {
        color: white;
        text-decoration:none;
    }

    .results {
        height: 90%;
        overflow: scroll;
    }

    .option {
        display: -webkit-flex;
    }

    .sorting {
        margin-top: 1%;
        margin-left: 4.5%;
        width: 91%;
        font-size: 0.73vw;
        border-bottom: 1px solid;
        border-color: white;
        cursor: default;

    }

    .fdr_filter{
        position: fixed;
        left: 76.5%;
    }

    .pathway-text{
        width: 92%;
        white-space: nowrap;
        overflow: hidden;    /* Hide overflow content */
        text-overflow: ellipsis;
        margin-left: 2%;
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
    width: 81.55%;
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
        cursor: pointer;
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
        padding-left: 5%;

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
        padding-bottom: 2%;
        font-size: 0.9vw;
        color: white;
        
    }

    .recolor_filter {
        filter: invert(71%) sepia(19%) saturate(7427%) hue-rotate(360deg) brightness(104%) contrast(105%);
    }


</style>