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
    // Create edges
    (ccl5)-[:LINK {
        // Evidence channels
        experiments: null,
        databases: 0.900,
        textmining: 0.906,
        coexpression: 0.092,
        neighbourhood: null,
        fusion: null,
        cooccurence: null,
        combined: 0.993,
        // Functional prediction
        activation: 0.849,
        binding: 0.849,
        catalysis: 0.278,
        ptmodification: 0.171,
        reaction: 0.922
    } ]->(ccr5),
    (ccl5)-[:LINK {
        // Evidence channels
        experiments: null,
        databases: null,
        textmining: 0.331,
        coexpression: 0.345,
        neighbourhood: null,
        fusion: null,
        cooccurence: null,
        combined: 0.547,
        // Functional prediction
        activation: null,
        binding: null,
        catalysis: null,
        ptmodification: null,
        reaction: null
    } ]->(il10ra),
    (il10ra)-[:LINK {
        // Evidence channels
        experiments: null,
        databases: null,
        textmining: 0.318,
        coexpression: 0.246,
        neighbourhood: null,
        fusion: null,
        cooccurence: null,
        combined: 0.469,
        // Functional prediction
        activation: null,
        binding: null,
        catalysis: null,
        ptmodification: null,
        reaction: null
    } ]->(ccr5)
