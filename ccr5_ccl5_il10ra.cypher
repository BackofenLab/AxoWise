CREATE

    // Proteins

    (ccr5:Protein {
        short_name: "CCR5",
        full_name: "Chemokine (C-C motif) receptor 5"
    }),
    (ccl5:Protein {
        short_name: "CCL5",
        full_name: "Chemokine (C-C motif) ligand 5"
    }),
    (il10ra:Protein {
        short_name: "IL10RA",
        full_name: "Interleukin 10 receptor, alpha subunit"
    }),

    // ---------------- CCL5 <-> CCR5 ----------------
    // Interaction
    (ccl5)-[:INTERACTION {
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
    (ccl5)-[:INTERACTION {
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
    (il10ra)-[:INTERACTION {
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
        source: "KEGG"
    }),
    (csp:Pathway {
        name: "Chemokine signaling pathway",
        source: "KEGG"
    }),
    (lcd:BiochemicalReaction {
        name: "The Ligand:GPCR:Gi complex dissociates",
        source: "curated"
    }),

    // Action - function relationships
    (ccl5_ccr5_activation)-[:IN]->(ccri),
    (ccl5_ccr5_binding)-[:IN]->(csp),
    (ccl5_ccr5_reaction)-[:IN]->(lcd)
