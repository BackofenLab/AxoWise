CREATE

    // Proteins

    (ccr5:Protein {
        short_name: "CCR5",
        full_name: "Chemokine (C-C motif) receptor 5",
        ensembl_id: "ENSMUSP00000107069"
    }),
    (ccl5:Protein {
        short_name: "CCL5",
        full_name: "Chemokine (C-C motif) ligand 5",
        ensembl_id: "ENSMUSP00000039600"
    }),
    (il10ra:Protein {
        short_name: "IL10RA",
        full_name: "Interleukin 10 receptor, alpha subunit",
        ensembl_id: "ENSMUSP00000034594"
    }),

    // ---------------- CCL5 <-> CCR5 ----------------
    // Interaction
    (ccl5)-[:ASSOCIATION {
        experiments: null,
        database: 0.900,
        textmining:	0.906,
        coexpression: 0.092,
        neighborhood: null,
        fusion:	null,
        cooccurence: null,
        combined: 0.993
    } ]->(ccr5),

    // Activation
    (ccl5_ccr5_activation:Action {
        name: "activation",
        score: 0.849
    }),
    (ccl5)-[:IN]->(ccl5_ccr5_activation),
    (ccr5)-[:IN]->(ccl5_ccr5_activation),

    // Binding
    (ccl5_ccr5_binding:Action {
        name: "binding",
        score: 0.849
    }),
    (ccl5)-[:IN]->(ccl5_ccr5_binding),
    (ccr5)-[:IN]->(ccl5_ccr5_binding),

    // Catalysis
    (ccl5_ccr5_catalysis:Action {
        name: "catalysis",
        score: 0.278
    }),
    (ccl5)-[:IN]->(ccl5_ccr5_catalysis),
    (ccr5)-[:IN]->(ccl5_ccr5_catalysis),

    // Post-translational modification
    (ccl5_ccr5_ptmodification:Action {
        name: "ptmodification",
        score: 0.171
    }),
    (ccl5)-[:IN]->(ccl5_ccr5_ptmodification),
    (ccr5)-[:IN]->(ccl5_ccr5_ptmodification),

    // Reaction
    (ccl5_ccr5_reaction:Action {
        name: "reaction",
        score: 0.922
    }),
    (ccl5)-[:IN]->(ccl5_ccr5_reaction),
    (ccr5)-[:IN]->(ccl5_ccr5_reaction),

    // ---------------- CCL5 <-> IL10RA ----------------
    // Interaction
    (ccl5)-[:ASSOCIATION {
        experiments: null,
        database: null,
        textmining: 0.331,
        coexpression: 0.345,
        neighborhood: null,
        fusion:	null,
        cooccurence: null,
        combined: 0.547
    } ]->(il10ra),

    // ---------------- IL10RA <-> CCR5 ----------------
    // Interaction
    (il10ra)-[:ASSOCIATION {
        experiments: null,
        database: null,
        textmining: 0.318,
        coexpression: 0.246,
        neighborhood: null,
        fusion:	null,
        cooccurence: null,
        combined: 0.469
    } ]->(ccr5),

    // Functional context
    (ccri:Pathway {
        name: "Cytokine-cytokine receptor interaction",
        source: "annotated pathway (KEGG)"
    }),
    (csp:Pathway {
        name: "Chemokine signaling pathway",
        source: "annotated pathway (KEGG)"
    }),
    (lcd:Pathway {
        name: "The Ligand:GPCR:Gi complex dissociates",
        source: "curated pathway"
    }),

    // Action - function relationships
    (ccl5_ccr5_activation)-[:IN]->(ccri),
    (ccl5_ccr5_binding)-[:IN]->(csp),
    (ccl5_ccr5_reaction)-[:IN]->(lcd)
