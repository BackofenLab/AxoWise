<template>
    <div id="citation-tools" class="pathways">
        <div class="pathwaybar">
            <div id="citation-list">
                <div class="tool-section-term">
                    <div class="citation-search">
                        <img class="pathway-search-icon" src="@/assets/toolbar/search.png">
                        <input type="text" v-model="search_raw" class="empty" placeholder="search abstracts"/>
                    </div>
                    <button class="community-citation" v-on:click="top_nodes(5)">
                        <div v-if="await_community == false" >top nodes</div>
                        <div v-if="await_community == true" class="loading_pane" ></div>
                    </button>
                </div>
                <div class="list-section">
                    
                    <div class="sorting">
                        <a class="pubid_filter" v-on:click="sort_alph = (sort_alph === 'asc') ? 'dsc' : 'asc'; sort_pr = ''; sort_cb = ''; sort_y = '' ">communities</a>
                        <a class="year_filter" v-on:click="sort_y = (sort_y === 'asc') ? 'dsc' : 'asc'; sort_pr = ''; sort_cb = ''; sort_alph = '' " >nodes</a>
                        <a class="fdr_filter" v-on:click="sort_pr = (sort_pr === 'asc') ? 'dsc' : 'asc'; sort_alph = ''; sort_cb = ''; sort_y = '' " >page rank</a>
                    </div>
        
                    <div class="results" tabindex="0" @keydown="handleKeyDown" ref="resultsContainer">
                        <table >
                            <tbody>
                                <tr v-for="(entry, index) in filt_communities" :key="index" class="option" :class="{ selected: selectedIndex === index }" v-on:click="select_community(entry.nodes, index)">
                                    <td>
                                        <div class="pathway-text" >
                                            <a href="#" ref="selectedNodes">Community {{entry.modularity_class}}</a>
                                        </div>
                                    </td>
                                    <td>
                                        <div class="pathway-text">
                                        </div>
                                    </td>
                                    <td>
                                        <div class="pathway-text">
                                            <a href="#">{{entry.nodes.length}}</a>
                                        </div>
                                    </td>
                                    <td>
                                        <div class="pathway-text">
                                            <a href="#">{{Math.log10(parseFloat(entry.cumulative_pagerank)).toFixed(2)}}</a>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div v-if="!context_results">
                        <i>No context available.</i>
                        </div>
                    </div>
                </div>
        
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'CitationCommunities',
    props: ['active_node','citation_data','await_community'],
    data() {
        return{
            search_raw: "",
            await_load: false,
            sort_alph: "",
            sort_pr: "",
            sort_cb: "",
            sort_y: "",
            selectedIndex: -1,
            communities: this.$store.state.citation_graph_data.graph.community_scores
        }
    },
    mounted(){
    },
    computed: {
        regex() {
            var com = this;
            return RegExp(com.search_raw.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
        },
        filt_communities() {
            var com = this;
            var filtered = Object.values(com.communities);

            if (com.search_raw !== "") {
            // If search term is not empty, filter by search term
            var regex = new RegExp(com.regex, 'i');
            filtered = filtered.filter(function(abstract) {
                return regex.test(abstract.nodes.join(" "));
            });
            }

            if(com.sort_y == "asc"){
                filtered.sort((t1, t2) => t2.nodes.length - t1.nodes.length)
            }else if (com.sort_y == "dsc"){
                filtered.sort((t1, t2) => t1.nodes.length - t2.nodes.length)
            }

            if(com.sort_pr == "asc"){
                filtered.sort((t1, t2) => t2.cumulative_pagerank - t1.cumulative_pagerank)
            }else if (com.sort_pr == "dsc"){
                filtered.sort((t1, t2) => t1.cumulative_pagerank - t2.cumulative_pagerank)
            }
            return new Set(filtered);
        },
    },
    methods: {
        select_community(community_nodes, index){
            var com = this;
            var abstract_names = new Set(community_nodes)
            const subset = []
            com.selectedIndex = index
            com.citation_data.nodes.forEach(node => {
                if(abstract_names.has(node.attributes['Name'].toUpperCase() )){
                    subset.push(node)
                }
            });
            com.emitter.emit("searchSubset", {subset: subset, mode: "citation"});
        },
        top_communities(count) {
        var com = this;
        var filtered = Object.values(com.communities);
        return filtered.sort((t1, t2) => t2.cumulative_pagerank - t1.cumulative_pagerank).slice(0, count);
        },
        
        top_nodes(count) {
            var com = this;
            var sorted_communities = com.top_communities(count);
            var top_nodes = [];

            for (var community of sorted_communities) {
                var abstract_names = new Set(community.nodes); // Replace with the actual field in your community objects
                var subset = [];
                
                com.citation_data.nodes.forEach(node => {
                    if (abstract_names.has(node.attributes['Name'].toUpperCase())) {
                        subset.push(node);
                    }
                });
                
                var highestPageRankNode = com.getHighestPageRankElements(subset);
                if (highestPageRankNode) {
                    top_nodes.push(highestPageRankNode);
                }
            }
            
            com.emitter.emit("generateSummary", top_nodes);
            var flatList = top_nodes.flat()
            com.emitter.emit("searchSubset", {subset: flatList, mode: "citation"});
        },
        
        getHighestPageRankElements(list) {
            if (list.length === 0) return null;

            if (list.length === 1) return [list[0]];

            list.sort((a, b) => b.pagerank - a.pagerank);
            return [list[0], list[1]];
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
                if (this.selectedIndex < this.filt_communities.size - 1){
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
    }, 
}
</script>


<style>
.community-citation {
    position: relative;
    display: -webkit-flex;
    cursor: pointer;
    border: none;
    color: white;
    border-style: solid;
    border-width: 1px;
    background: #0A0A1A;
    border-color: white;
    margin-left: 0.2vw;
    align-items: center;
    justify-content: center;
    font-size: 0.7vw;
    height: 1.3vw;
    width: 4.2vw;
}
</style>