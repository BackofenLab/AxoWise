import { createStore } from 'vuex'

export const store = createStore({
  state: {
      gephi_json: null,
      enrichment_terms: null,
      term_graph_data: null,
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
        {value: "NetworkNeighborAL", label: "Network"}],
        sigma_graph_node: null,
        sigma_graph_term: null,
        sigma_graph_subset: null,
        enrichment: null,
        active_node_enrichment: null,
        dcoloumns: null,
    },
  mutations:{
    assign(state, value) {
        state.gephi_json = value
    },
    assign_enrichment(state, value) {
      state.enrichment_terms = value
    },
    assign_term_graph(state, value) {
      state.term_graph_data = value
    },
    assign_graph_node(state, value){
      state.sigma_graph_node = value
    },
    assign_graph_subset(state, value){
      state.sigma_graph_subset = value
    },
    assign_graph_term(state, value){
      state.sigma_graph_term = value
    },
    assign_active_enrichment(state, value){
      state.enrichment = value
    },
    assign_active_enrichment_node(state, value){
      state.active_node_enrichment = value
    },
    assign_dcoloumn(state, value){
      state.dcoloumns = value
    }
  }
})