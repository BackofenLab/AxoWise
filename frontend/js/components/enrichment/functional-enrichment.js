Vue.component("functional-enrichment", {
    props: ["gephi_json", "func_json","revert_term","func_enrichment",
            "reset_term", "term_graph_save", "graph_flag"],
    data: function() {
        return  {
            filter_terms: [
                {value: "TISSUES", label: "Tissue expression"},
                {value: "KEGG", label: "KEGG Pathway"},
                {value: "COMPARTMENTS", label: "Subcellular localization"},
                /* Process, Component, Function and reactome need to be changed for inhouse enrichment */
                {value: "Biological Process (Gene Ontology)", label: "Biological Process"},
                {value: "Cellular Component (Gene Ontology)", label: "Cellular Component(Gene Ontology)"},
                {value: "Molecular Function (Gene Ontology)", label: "Molecular Function"},
                {value: "Keyword", label: "Annotated Keywords(UniProt)"},
                {value: "SMART", label: "Protein Domains(SMART)"},
                {value: "InterPro", label: "Protein Domains and Features(InterPro)"},
                {value: "Pfam", label: "Protein Domains(Pfam)"},
                {value: "PMID", label: "Reference Publications(PubMed)"},
                {value: "Reactome Pathways", label: "Reactome Pathway"}, /* RCTM */
                {value: "WikiPathways", label: "WikiPathays"},
                {value: "MPO", label: "Mammalian Phenotype Ontology"},
                {value: "NetworkNeighborAL", label: "Network"}] 
            ,
            message: "",
            terms: [],
            saved_terms: [],
            proteins: [],
            search_raw: "",
            filter: "",
            await_check: true,
            await_load: false,
            term_numbers: "",

        }
    },
    methods: {
        select_term: function(term) {
            var com = this;
            com.$emit("active-term-changed", term);
        },
        select_cat: function(category) {
            var com = this;

            var filtered_terms = [];
            var check_terms = com.saved_terms[com.saved_terms.length -1];

            //Filter the terms according to user selection
            for (var idx in check_terms) {
                if(check_terms[idx].category == category && category != null){
                    filtered_terms.push(check_terms[idx]);
                }
            }
            //Reset function for Terms
            if(category != null){
                com.terms = filtered_terms;
            }else{com.terms = com.saved_terms[com.saved_terms.length -1]}

            //Count term number
            com.term_number();
        },
        get_functionterms: function(term) {
            var com = this;
            com.$emit("func-json-changed", term);
        },
        export_enrichment: function(){
            com = this;

            //export terms as csv
            csvTermsData = com.terms;
            terms_csv = 'category,fdr_rate,name,proteins\n';

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
        term_number: function(){
            var com = this;

            com.term_numbers = com.terms.length.toString();

        },
        open_pane: function(){

            const div = document.querySelector('#enrichment');
            if(!div.classList.contains('tool-pane-show')){
                $('.tool-pane').addClass('tool-pane-show');
            }
            else{
                $('.tool-pane').removeClass('tool-pane-show');
            }

        }
    },
    watch: {
        "gephi_json": function(json) {
            var com = this;
            if (!json) return ; //handling null json from backend
            // if (!json.enrichment) return: ‚
            
            com.get_functionterms(json.nodes);

        },
        "func_json": function(nodes) {
            var com = this;

            //Reverting functional terms
            if(nodes==null) {
                com.await_check = false, com.terms = com.saved_terms[0], com.saved_terms = [com.terms];
                com.term_number();
                return;
            }

            //Set up parameter for functional enrichment
            com.proteins = [];
            for (var idx in nodes) {
                com.proteins.push(nodes[idx].id);
            }

            if (com.graph_flag) {
                com.await_check = true, com.await_load = true;
                formData = new FormData();

                formData.append('proteins', com.proteins);
                formData.append('species_id', nodes[0].species);

                com.filter="";

                // TODO: Add loading, so that user can't spam between graphs?
                // $("#term-btn").addClass("loading");
                $("#term-btn").addClass("loading");
                
                
                //POST request for functional enrichment
                $.ajax({
                    type: 'POST',
                    url: "/api/subgraph/enrichment",
                    data: formData,
                    contentType: false,
                    cache: false,
                    processData: false,
                })
                .done(function (json) {
                    // $("#term-btn").removeClass("loading");      
                    com.await_load = false;                  
                    if(com.await_check){
                        com.$emit("func-enrichment-changed", json);
                        //Save terms
                        com.terms = [];
                        for (var idx in json) {
                            com.terms.push(json[idx]);
                            }
                            com.saved_terms.push(com.terms);

                            //Sort terms according to the fdr rate
                            com.terms.sort(function(t1, t2) {
                                var p_t1 = parseFloat(t1.fdr_rate);
                                var p_t2 = parseFloat(t2.fdr_rate);
                                return p_t1 - p_t2;
                            });

                            // draw functional term graph

                            formData.append('func-terms', JSON.stringify(com.terms))

                            $.ajax({
                                type: "POST",
                                url: "/api/subgraph/terms",
                                data: formData,
                                contentType: false,
                                cache: false,
                                processData: false,
                              }).done(function (json) {
                                $("#term-btn").removeClass("loading");
                                if (Object.keys(json).length != 0) {
                                  // save term graph
                                  json.edge_thick = com.gephi_json.edge_thick;
                                  com.$emit("term-graph-save", json);
                                }
                              }).fail(function ( jqXHR, textStatus, errorThrown ) {
                                  console.log(jqXHR);
                                  console.log(textStatus);
                                  console.log(errorThrown);
                              });

                            //Count term number
                            com.term_number();
                        }
                });
            }
        },
        "revert_term": function(subset) {
            var com = this;

            if (!subset) return ;

            //Load previous subset terms from saved_terms
            com.await_check = false;
            com.saved_terms.pop()
            com.terms = com.saved_terms[com.saved_terms.length-1];

            //Count term number
            com.term_number();
        },
        "reset_term": function(subset) {
            var com = this;

            if (!subset) return ;

            //Load main graph terms from saved_terms
            com.await_check = false;
            com.terms = com.saved_terms[0];

            //Count term number
            com.term_number();
        },
    },
    computed: {
        regex: function() {
            var com = this;
            return RegExp(com.search_raw.toLowerCase());
        },
        filtered_terms: function() {
            var com = this;

            if (com.search_raw == "") return com.terms;

            var regex = com.regex;
            var filtered = com.terms.filter(term => regex.test(term.name.toLowerCase()));
            return filtered;
        }
    },
    template: `
        <div v-show="gephi_json != null" id="enrichment" class="tool-pane">
            <div class="headertext">
            <button v-on:click="open_pane()">Functional Enrichment:</button>
            </div>
            <div class="main-section">
                <div class="enrichment-filtering">
                    <input type="text" value="Search functional terms by name" v-model="search_raw" class="empty"/>
                    <v-select id="vsel" placeholder="..." v-model="filter" :options="filter_terms" :reduce="label => label.value" label="value" v-on:input="select_cat(filter)"></v-select>

                </div>
                <div v-if="await_load==false" class="term_number">
                    <span>Terms: {{term_numbers}}</span>
                </div>
            <div v-if="await_load == true" class="loading_pane"></div>
            <div v-if="await_load == false" class="results">
                <i v-if="message.length > 0">{{message}}</i>
                <div v-for="entry in filtered_terms">
                    <a href="#" v-on:click="select_term(entry)">{{entry.name}}</a>
                </div>
                <div v-if="terms.length == 0">
                    <i>No terms available.</i>
                </div>
            </div>
            <button v-if="await_load == false" id="export-enrich-btn" v-on:click="export_enrichment()">Export</button>
        </div>
        </input>
    </div>
    `
});