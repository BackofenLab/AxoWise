<template>
    <div id="pathways-list">
        <div class="tool-section-term">
            <div class="pathway-search">
                <img class="pathway-search-icon" src="@/assets/toolbar/search.png">
                <input type="text" v-model="search_raw" class="empty" placeholder="Find your pathways"/>
            </div>
            <div class="filter-section">
                <div id="pathway-filter" class="pre-full" v-on:click="handling_filter_menu()" :class="{ full: category_filtering == true }">
                    <span>{{ category }}</span>
                    <img  class="remove-filter" src="@/assets/pathwaybar/cross.png" v-on:click.stop="active_categories(null)" v-if="category !== 'Filter'">
                </div>
                <div id="pathway-filter-categories" v-show="category_filtering == true && terms !== null">
                    <div class="element" v-for="(entry, index) in filter_terms" :key="index" v-on:click="active_categories(entry.label);" :class="{ active_cat: active_categories_set.has(entry.label)}">
                        <a>{{ entry.label }}</a>
                    </div>
                </div>
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
            active_categories_set: new Set(),
            filter_terms: [],
            bookmark_off: true,
            favourite_tab: new Set(),
            selectedIndex: -1,
            mode: 'term'
        }
    },
    mounted(){
        console.log(this.term_data)
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
            
            if (com.category != "Filter") {
            // If category is set, filter by category
            filtered = filtered.filter(function(term) {
                return  com.active_categories_set.has(term.attributes['Category']);
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
            var remove_duplicates = [...new Set(terms.map(term => term.attributes["Category"]))]
            remove_duplicates.forEach(term => {
                com.filter_terms.push({'label': term})
            })

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
</style>