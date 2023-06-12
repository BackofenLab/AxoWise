<template>
    <div id="enrichment" class="tool-pane">
            <div class="headertext">
            <button v-on:click="open_pane()">Functional Enrichment:</button>
            </div>
            <div class="main-section">
                <div class="enrichment-filtering">
                    <input type="text" v-model="search_raw" class="empty"/>
                    <v-select id="vsel" placeholder="..." v-model="category" :options="filter_terms" :reduce="label => label.label" label="label" ></v-select>
                </div>
                <!-- <div v-if="await_load==false" class="term_number">
                    <span>Terms: {{term_numbers}}</span>
                </div> -->
            <div v-if="await_load == true" class="loading_pane"></div>
            <div class="results" v-if="terms !== null && await_load == false">
                <div v-for="entry in filtered_terms" :key=entry>
                    <a href="#" v-on:click="select_term(entry)">{{entry.name}}</a>
                </div>
                <div v-if="terms.length == 0">
                    <i>No terms available.</i>
                </div>
            </div>
            <button v-if="await_load == false" id="export-enrich-btn" v-on:click="export_enrichment()">Export</button>
            <div class="get_term_graph">
                <input type="text" v-if="await_load == false" v-model="graph_name">
                <button v-if="await_load == false" id="apply-enrich-btn" v-on:click="get_term_data()">Get Graph</button>
            </div>
        </div>
    </div>
</template>

<script>
    export default{
        name: 'EnrichmentTool',
        props: ['gephi_data','active_term'],
        emits: ['active_term_changed', 'active_layer_changed'],
        data() {
            return {
                api: {
                    subgraph: "api/subgraph/enrichment",
                },
                terms: null,
                search_raw: "",
                filter_terms: [],
                category: "",
                await_load: true,
                sourceToken: null,
                graph_name: 'graph'
            }
        },
        methods: {
            open_pane(){
                const div = document.querySelector('#enrichment');
                if(!div.classList.contains('tool-pane-show')){
                    div.classList.add("tool-pane-show");
                }
                else{
                    div.classList.remove("tool-pane-show");
                }
            },
            select_term(term) {
                var com = this;

                com.$emit("active_term_changed", term);
            },
            get_term_data() {
                var com = this

                var formData = new FormData()
                formData.append('func-terms', JSON.stringify(com.terms))

                this.axios
                    .post("/api/subgraph/terms", formData)
                    .then((response) => {
                        this.$store.commit('assign_term_graph', response.data)
                        if(this.graph_name == null) this.graph_name = 'Main Graph'
                        this.$store.commit('assign_new_term_graph', {label: this.graph_name, graph: response.data})
                    })

            },
            export_enrichment: function(){
                var com = this;

                //export terms as csv
                var csvTermsData = com.filtered_terms;
                var terms_csv = 'category,fdr_rate,name,proteins\n';

                csvTermsData.forEach(function(row) {
                    terms_csv += row['category'] + ',' + row['fdr_rate'] + ',"'  + row['name'] + '","' +row['proteins']+'"';
                    terms_csv += '\n';   
                });


                //Create html element to hidden download csv file
                var hiddenElement = document.createElement('a');
                hiddenElement.target = '_blank';
                hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(terms_csv);
                hiddenElement.download = 'Terms.csv';  
                hiddenElement.click();
            },
            abort_enrichment() {
                this.sourceToken.cancel('Request canceled');
                this.await_load = false 
            },
            apply_layer(subset, hide) {
                var com = this;

                
                if (hide) com.$emit("active_layer_changed", subset);

                var formData = new FormData()
                
                formData.append('proteins', subset)
                formData.append('species_id', com.gephi_data.nodes[0].species)
                
                com.await_load = true

                com.sourceToken = this.axios.CancelToken.source();

                this.axios
                    .post(com.api.subgraph, formData, { cancelToken: com.sourceToken.token })
                    .then((response) => {
                        com.terms = response.data.sort((t1, t2) => t1.fdr_rate - t2.fdr_rate)
                        com.await_load = false
                        this.$store.commit('assign_new_enrichment', {"term":subset, "term_set": com.terms})
                    })
                    .catch(() => {
                        //TODO: Catch the abort if needed
                    });
            },
            revert_layer(hide) {
                var com = this;

                if(com.await_load){
                    this.emitter.emit("abortEnrichment");
                    if(this.$store.state.enrichment_set.length != 0) com.$emit("active_layer_changed", this.$store.state.enrichment_set[this.$store.state.enrichment_set.length -1].term );
                    else if(hide) com.$emit("active_layer_changed", null);
                    return
                }
                this.$store.commit('pop_old_enrichment')
                if(this.$store.state.enrichment_set.length == 0) {
                    com.terms = this.$store.state.enrichment_terms;
                    if(hide) com.$emit("active_layer_changed", null);
                } else {
                    var enrich_item = this.$store.state.enrichment_set[this.$store.state.enrichment_set.length -1];
                    com.terms = enrich_item.term_set
                    if(hide) com.$emit("active_layer_changed", enrich_item.term );
                }
            },
            filter_options() {
                var com = this
                com.filter_terms = []
                var remove_duplicates = [...new Set(com.terms.map(term => term.category))]
                remove_duplicates.forEach(term => {
                    com.filter_terms.push({'label': term})
                })
            }
        },
        mounted() {
            var com = this

            var formData = new FormData()

            formData.append('proteins', com.gephi_data.nodes.map(node => node.id))
            formData.append('species_id', com.gephi_data.nodes[0].species)
                

            //POST request for functional enrichment
            this.axios
              .post(com.api.subgraph, formData)
              .then((response) => {
                this.$store.commit('assign_enrichment', response.data.sort((t1, t2) => t1.fdr_rate - t2.fdr_rate))
                com.terms = this.$store.state.enrichment_terms
                com.get_term_data(formData)
                com.filter_options()
                this.await_load = false
                })
            
            this.emitter.on("abortEnrichment", () => {
                this.abort_enrichment()
                
            });

            this.emitter.on("enrichTerms", (subset) => {
                if(subset != null) this.apply_layer(subset, true);
                else this.revert_layer(true);
            });

            this.emitter.on("enrichSubset", (subset) => {
                if(subset != null) this.apply_layer(subset, false);
                else this.revert_layer(false);
            });
    
        },
        computed: {
            regex() {
                var com = this;
                return RegExp(com.search_raw.toLowerCase());
            },
            filtered_terms() {
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

                return filtered;
            }

    },
}
</script>

<style >
    #apply-enrich-btn {
        position: relative;
        background-color: rgba(0,0,0,.5);
        margin-top: 10px;
        width: 70%;
        color: #fff;
        padding: 5px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: .5s;
    }
    .get_term_graph {
        position: relative;
        display: flex;
        padding: 10px;
    }
    .get_term_graph input[type="text"]{
        position: relative;
        border-radius: 20px;
        text-align: center;
        width: 130px;
        height: 30px;
        margin-right: 20px;
        margin-top: 10px;

    }
</style>