CREATE

    // Create nodes

    (ccr5:ChemokineReceptor {
        name: "Chemokine (C-C motif) receptor 5",
        structure: "CC"
    }),
    (ccl5:ChemokineLigand {
        name: "Chemokine (C-C motif) ligand 5",
        structure: "CC"
    }),
    (il10ra:CytokineReceptorSubunit {
        receptor: "Interleukin 10 receptor",
        subunit: "alpha"
    }),

    // Create relationships

    // CCL5 <-> CCR5
    (ccl5)-[:FUNC_EVIDENCE {
        score: 0.993
    } ]->(ccr5),
    (ccl5)-[:ACTIVATION {
        score: 0.849,
        pathway: "Cytokine-cytokine receptor interaction"
    } ]->(ccr5),
    (ccl5)-[:BINDING {
        score: 0.849,
        pathway: "Chemokine signaling pathway"
    } ]->(ccr5),
    (ccl5)-[:CATALYSIS {
        score: 0.278
    } ]->(ccr5),
    (ccl5)-[:PT_MODIFICATION {
        score: 0.171
    } ]->(ccr5),
    (ccl5)-[:REACTION {
        score: 0.922,
        biochemical_reaction: "The Ligand:GPCR:Gi complex dissociates"
    } ]->(ccr5),

    // CCL5 <-> IL10RA
    (ccl5)-[:FUNC_EVIDENCE {
        score: 0.547
    } ]->(il10ra),

    // IL10RA <-> CCR5
    (il10ra)-[:FUNC_EVIDENCE {
        score: 0.469
    } ]->(ccr5)
