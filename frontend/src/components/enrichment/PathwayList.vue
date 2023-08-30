<template>
    <div id="pathways-list">
        <img id="pathway-search" src="@/assets/pathwaybar/pathway-button.png">
        <img id="pathway-filter" src="@/assets/pathwaybar/pathway-button-2.png">
        <div class="bookmark-button" v-on:click="bookmark_off = !bookmark_off">
            <img class="bookmark-image" src="@/assets/pathwaybar/favorite.png" :class="{recolor_filter: bookmark_off == false}">
        </div>
        <div class="visualize-button"></div>
        <div class="export-button"></div>
        <div class="list-section">
            
            <div class="sorting">
                <a class="enrichment_filter">functional enrichment pathways</a>
                <a class="fdr_filter" v-on:click="sort(sort_order)" >fdr rate</a>
            </div>

            <div v-if="await_load == true" class="loading_pane" ></div>
            <div class="results" v-if="terms !== null && await_load == false" tabindex="0" @keydown="handleKeyDown" ref="resultsContainer">
                <table >
                    <tbody>
                        <tr v-for="(entry, index) in terms" :key="index" class="option" :class="{ selected: selectedIndex === index }" :style="{ display: shouldDisplayOption(entry) && (bookmark_off || favourite_tab.has(entry.id)) ? '-webkit-flex' : 'none' }">
                            <td>
                                <div class="favourite-symbol">
                                <label class="custom-checkbox">
                                    <div class="checkbox-image" v-on:click="add_enrichment(entry)" :class="{ checked: favourite_tab.has(entry.id)}" ref="checkboxStates"></div>
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
    emits: ['active_term_changed', 'active_layer_changed', 'active_termlayers_changed'],
    data() {
        return{
            api: {
                subgraph: "api/subgraph/enrichment",
            },
            terms: [],
            await_load: false,
            search_raw: "",
            bookmark_off: true,
            selectedIndex: -1,
            sort_order: false,
            category: null,
            favourite_tab: new Set()
        }
    },
    mounted() {
        var com = this
        com.generatePathways(com.gephi_data.nodes[0].species, com.gephi_data.nodes.map(node => node.id))

    },
    watch: {
        terms() {
            this.filtered_terms = this.terms
        }
    },
    computed: {
        regex() {
            var com = this;
            return RegExp(com.search_raw.toLowerCase());
        },
        filt_terms() {
            var com = this;
            var filtered = com.terms;
            
            if (com.category) {
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
                // com.filter_options()
                com.await_load = false
            })

        },
        shouldDisplayOption(entry) {
            return this.filt_terms.has(entry);
        },
        sort(){
            this.sort_order = !this.sort_order
            if(this.sort_order) this.terms.sort((t1, t2) => t2.fdr_rate - t1.fdr_rate)
            else this.terms.sort((t1, t2) => t1.fdr_rate - t2.fdr_rate)
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
                if (this.selectedIndex < this.filtered_terms.length - 1){
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
            if (!this.favourite_tab.has(enrichment.id)) {
                // Checkbox is checked, add its state to the object
                this.favourite_tab.add(enrichment.id)
            } else {
                // Checkbox is unchecked, remove its state from the object
                this.favourite_tab.delete(enrichment.id)
            }
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

    #pathway-search {
        width: 37.54%;
        height: 11.16%;
        position: absolute;
    }

    #pathway-filter {
        width: 20.54%;
        left: 35.7%;
        height: 11.16%;
        position: absolute;
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
    }
    .export-button {
        width: 15.8%;
        height: 11.16%;
        left: 84.1%;
        position: absolute;
        border-radius: 5px;
        background: #0A0A1A;
    }

    .list-section a {
        color: white;
        text-decoration:none;
    }

    .results {
        height: 90%;
        overflow: scroll;
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

    .recolor_filter {
        filter: invert(71%) sepia(19%) saturate(7427%) hue-rotate(360deg) brightness(104%) contrast(105%);
    }


</style>