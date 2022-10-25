Vue.component("functional-enrichment", {
    props: ["gephi_json", "func_json","revert_term","func_enrichment", "reset_term"],
    data: function() {
        return  {
            filter_terms: {
                "RESET": "No Filter",
                "TISSUES": "Tissue expression",
                "KEGG": "KEGG Pathway",
                "COMPARTMENTS": "Subcellular localization",
                "Process": "Biological Process",
                "Component": "Cellular Component(Gene Ontology)",
                "Function": "Molecular Function",
                "Keyword": "Annotated Keywords(UniProt)",
                "SMART": "Protein Domains(SMART)",
                "InterPro": "Protein Domains and Features(InterPro)",
                "Pfam": "Protein Domains(Pfam)",
                "PMID": "Reference Publications(PubMed)",
                "RCTM": "Reactome Pathway",
                "WikiPathways": "WikiPathays",
                "MPO": "Mammalian Phenotype Ontology",
                "NetworkNeighborAL": "Network",
                
            },
            message: "",
            terms: [],
            saved_terms: [],
            proteins: [],
            search_raw: "",
            filter: "",
            await_check: true,
            enrich_check: false

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
            for (var idx in check_terms) {
                if(check_terms[idx].category == category && category != "RESET"){
                    filtered_terms.push(check_terms[idx]);
                }
            }
            if(category != "RESET"){
                com.terms = filtered_terms;
            }else{com.terms = com.saved_terms[com.saved_terms.length -1]}
        },
        get_functionterms: function(term) {
            var com = this;
            com.$emit("func-json-changed", term);
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
            // if (!json) return ; //handling null json from backend
            // // if (!json.enrichment) return;

            if(nodes==null) {
                com.await_check = false;
                com.terms = com.saved_terms[0];
                com.saved_terms = [com.terms];
                return;
            }

            com.proteins = [];
            for (var idx in nodes) {
                com.proteins.push(nodes[idx].id);
            }

            com.await_check = true;
            formData = new FormData();
            formData.append('proteins', com.proteins);
            formData.append('species_id', nodes[0].species);

            $("#enrichment").addClass("loading");
            

            $.ajax({
                type: 'POST',
                url: "/api/subgraph/enrichment",
                data: formData,
                contentType: false,
                cache: false,
                processData: false,
              })
              .done(function (json) {         
                $("#enrichment").removeClass("loading");                     
                  if(com.await_check){
                      com.$emit("func-enrichment-changed", json);
                      com.terms = [];
                      for (var idx in json) {
                          com.terms.push(json[idx]);
                        }
                        com.saved_terms.push(com.terms);
                        com.terms.sort(function(t1, t2) {
                            var p_t1 = parseFloat(t1.fdr_rate);
                            var p_t2 = parseFloat(t2.fdr_rate);
                            return p_t1 - p_t2;
                        });
                    }
            });
        },
        "revert_term": function(subset) {
            var com = this;
            if (!subset) return ;
            com.await_check = false;
            com.saved_terms.pop()
            com.terms = com.saved_terms[com.saved_terms.length-1];
        },
        "reset_term": function(subset) {
            var com = this;
            if (!subset) return ;
            com.await_check = false;
            com.terms = com.saved_terms[0];
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
    <div class="toolbar-button">
        <div v-show="gephi_json != null">
        <button v-on:click="enrich_check=!enrich_check" id="enrich_button">Σ</button>
         </div>
        <div v-show="gephi_json != null && enrich_check === true" id="enrichment" class="white-theme">
            <h4>Functional enrichment:</h4>
            <br/>
            <h5>Filter:</h5>
            <select v-model="filter" v-on:change="select_cat(filter)">
                <option disabled value="">Please select term</option>
                <option v-for="(value, key, index) in filter_terms" v-bind:value="key">{{value}}</option>
            </select>
            <br/><br/>
            <input type="text" value="Search functional terms by name" v-model="search_raw" class="empty"/>
            <div class="modalpane"> </div>
            <div class="results">
                <i v-if="message.length > 0">{{message}}</i>
                <div v-for="entry in filtered_terms">
                    <a href="#" v-on:click="select_term(entry)">{{entry.name}}</a>
                </div>
                <div v-if="terms.length == 0">
                    <i>No terms available.</i>
                </div>
            </div>
        </div>
    </div>
    `
});