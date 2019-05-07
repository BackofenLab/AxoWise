"""
Collection of Cypher queries for writing and reading the resulting
Neo4j graph database.
"""

from neomodel import db, install_all_labels, remove_all_labels
from schema import Protein, Pathway, Compound, Disease, Drug, Class

# ========================= Creating queries =========================

@db.transaction
def add_compound(batch: list):
    """
    Create a compound with the specified id and
    name.
    """
    Compound.create(*batch)

@db.transaction
def add_disease(batch: list):
    """
    Create a disease with the specified id and
    name.
    """

    Disease.create(*batch)

@db.transaction
def add_drug(*batch):
    """
    Create a drug with the specified id and
    name.
    """

    Drug.create(*batch)

@db.transaction
def add_class_parent_and_child(batch):
    """
    Create parent - child relationship between
    two pathway classes.
    """

    parent_batch = map(lambda obj: {"name_parent": obj["name_parent"]}, batch)
    child_batch = map(lambda obj: {"name_child": obj["name_child"]}, batch)

    parents = Class.get_or_create(*parent_batch) # MERGE
    children = Class.get_or_create(*child_batch) # MERGE
    for parent, child in zip(parents, children):
        parent.children.connect(child)

@db.transaction
def add_pathway(batch: list):
    """
    Create a pathway with the specified id, name,
    description and species to which it belongs.
    After that, connect it to the corresponding class.
    """

    class_batch = map(lambda obj: {"class": obj["class"] }, batch)

    classes = Class.get_or_create(*class_batch)
    pathways = Pathway.create(*batch)
    for pathway, cls in zip(pathways, classes):
        pathway.cls.connect(cls)

@db.transaction
def add_protein(batch):
    """
    Create a protein with the specified id, external id,
    name, description and species to which it belongs.
    """

    Protein.create(*batch)

@db.transaction
def add_action(batch):
    """
    For an existing protein - protein pair, create / update (merge) the given
    action associated with the given pathway.
    """

    for entry in batch:
        protein1 = Protein.nodes.get(iid=entry["id1"])
        protein2 = Protein.nodes.get(iid=entry["id2"])
        del entry["id1"], entry["id2"] # Entry now contains only 'mode' and 'score'
        protein1.actions.connect(protein2, entry)

@db.transaction
def add_association(batch):
    """
    For an existing protein - protein pair, create the association
    between them.
    """

    for entry in batch:
        protein1 = Protein.nodes.get(iid=entry["id1"])
        protein2 = Protein.nodes.get(iid=entry["id2"])
        del entry["id1"], entry["id2"] # Entry now contains only channels scores and the combined score
        protein1.associations.connect(protein2, entry)

# ========================= Connecting queries =========================

@db.transaction
def connect_protein_and_pathway(batch):
    """
    Creates IN association for the given protein and
    pathway.
    """

    for entry in batch:
        protein = Protein.nodes.get(external_id=entry["protein_external_id"])
        pathway = Pathway.nodes.get(iid=entry["pathway_id"])
        protein.pathways.connect(pathway)

@db.transaction
def connect_compound_and_pathway(batch):
    """
    Creates IN association for the given compound and
    pathway.
    """

    for entry in batch:
        compound = Compound.nodes.get(iid=entry["compound_id"])
        pathway = Pathway.nodes.get(iid=entry["pathway_id"])
        compound.pathways.connect(pathway)

@db.transaction
def connect_disease_and_pathway(batch):
    """
    Creates IN association for the given disease and
    pathway.
    """

    for entry in batch:
        disease = Disease.nodes.get(iid=entry["disease_id"])
        pathway = Pathway.nodes.get(iid=entry["pathway_id"])
        disease.pathways.connect(pathway)

@db.transaction
def connect_drug_and_pathway(batch):
    """
    Creates IN association for the given drug and
    pathway.
    """

    for entry in batch:
        drug = Disease.nodes.get(iid=entry["drug_id"])
        pathway = Pathway.nodes.get(iid=entry["pathway_id"])
        drug.pathways.connect(pathway)

# ========================= Schema queries =========================

def create_indexes_and_constraints():
    """
    Creates node indexes and constraints for the Neo4j graph database.
    """
    install_all_labels(stdout=True)

def drop_indexes_and_constraints():
    """
    Drops node indexes and constraints for the Neo4j graph database.
    """
    remove_all_labels(stdout=True)

# ========================= Server warm-up =========================

def warm_up(graph):
    query = """
        MATCH (n)
        OPTIONAL MATCH (n)-[r]->()
        RETURN count(n.id) + count(r.combined);
    """
    print("Warming up Neo4j...")
    db(query)
    print("Done.")

# ========================= List queries =========================
def get_protein_list(graph):
    """
    Retrieve a list of proteins including the protein ID
    and the protein name.
    """

    query = """
        MATCH (protein:Protein)
        RETURN protein.id AS id,
               protein.name AS name,
               protein.species_id AS species_id
    """

    return graph.run(query)

def get_pathway_list(graph):
    """
    Retrieve a list of pathways including the pathway ID
    and the pathway name.
    """

    query = """
        MATCH (pathway:Pathway)
        RETURN pathway.id AS id,
               pathway.name AS name,
               pathway.species_id AS species_id
    """

    return graph.run(query)

def get_class_list(graph):
    """
    Retrieve a list of all available pathway
    class names.
    """

    query = """
        MATCH (class:Class)
        RETURN class.name AS name
    """

    return graph.run(query)

# ========================= Subgraph queries =========================

def get_protein_subgraph(graph, protein_id, threshold=0):
    """
    For the given protein, return the Neo4j subgraph
    of the protein, all other associated proteins and
    the common pathways.
    """

    # Neo4j query
    query = """
        MATCH (protein:Protein {
            id: {protein_id}
        })
        USING INDEX protein:Protein(id)
        WITH protein
        MATCH (protein)-[:IN]->(pathway:Pathway)
        WITH protein, COLLECT(DISTINCT pathway) AS pathways
        MATCH (protein)-[association:ASSOCIATION]-(other:Protein)
        WHERE association.combined >= {threshold}
        RETURN protein, pathways, COLLECT({
            combined_score: association.combined,
            other: other
        }) AS associations
    """

    assert 0 <= threshold <= 1000,\
           "Combined score threshold should be in range [0, 1000]!"

    param_dict = dict(
        protein_id=protein_id,
        threshold=threshold
    )
    return graph.run(query, param_dict)

def get_proteins_subgraph(graph, protein_ids, threshold=0, external=False):
    """
    For the given list of proteins, return the Neo4j
    subgraph of the proteins, all associations between
    them and common pathways.
    """

    # Neo4j query
    query = """
        MATCH (protein:Protein)
    """ + \
    ("WHERE protein.external_id IN {protein_ids}" if external else "WHERE protein.id IN {protein_ids}") + \
    """
        WITH COLLECT(protein) AS proteins
        WITH proteins, SIZE(proteins) AS num_proteins
        UNWIND RANGE(0, num_proteins - 1) AS i
        UNWIND RANGE(i + 1, num_proteins - 1) AS j
        WITH proteins, proteins[i] AS protein1, proteins[j] AS protein2
        OPTIONAL MATCH (protein1)-[association:ASSOCIATION]-(protein2)
        WHERE association.combined >= {threshold}
        WITH proteins, protein1, association, protein2
        OPTIONAL MATCH (protein1)-[:IN]->(pathway:Pathway)<-[:IN]-(protein2)
        RETURN proteins AS proteins, COLLECT(DISTINCT pathway) AS pathways, COLLECT({
            protein1_id: protein1.id,
            combined_score: association.combined,
            protein2_id: protein2.id,
            pathway_id: pathway.id
        }) AS associations
    """

    assert 0 <= threshold <= 1000,\
           "Combined score threshold should be in range [0, 1000]!"

    param_dict = dict(
        protein_ids=protein_ids,
        threshold=threshold
    )
    return graph.run(query, param_dict)

def get_pathway_subgraph(graph, pathway_id, threshold=0):
    """
    For the given pathway, return the Neo4j subgraph
    of the pathway, all contained proteins and
    the class hierarchy of the pathway.
    """

    # Neo4j query
    query = """
        MATCH (pathway:Pathway {
            id: {pathway_id}
        })
        USING INDEX pathway:Pathway(id)
        WITH pathway
        OPTIONAL MATCH (class:Class)<-[:IN*]-(pathway)
        WITH pathway, COLLECT(DISTINCT class) AS classes
        MATCH (protein:Protein)-->(pathway)
        WITH classes, COLLECT(protein) AS proteins
        WITH classes, proteins, SIZE(proteins) AS num_proteins
        UNWIND RANGE(0, num_proteins - 1) AS i
        UNWIND RANGE(i + 1, num_proteins - 1) AS j
        WITH classes, proteins, proteins[i] AS protein1, proteins[j] AS protein2
        MATCH (protein1)-[association:ASSOCIATION]-(protein2)
        // WHERE association.combined >= {threshold}
        RETURN classes, proteins, COLLECT({
            protein1_id: protein1.id,
            combined_score: association.combined,
            protein2_id: protein2.id
        }) AS associations
    """

    assert 0 <= threshold <= 1000,\
           "Combined score threshold should be in range [0, 1000]!"

    param_dict = dict(
        pathway_id=pathway_id,
        threshold=threshold
    )
    return graph.run(query, param_dict)

def get_class_subgraph(graph, name):
    """
    For the given pathway class, return the Neo4j subgraph
    of the class hierarchy and pathways attached to the
    leaves of the hierarchy tree.
    """

    query = """
        MATCH (class:Class {
            name: {name}
        })
        USING INDEX class:Class(name)
        // "fuzzy" search: WHERE toUpper(class.name) =~ (".*" + toUpper({name}) + ".*")
        WITH class
        OPTIONAL MATCH (class)<-[:IN*]-(pathway:Pathway)
        RETURN class, COLLECT(DISTINCT pathway) as pathways
    """

    param_dict = dict(name=name)
    return graph.run(query, param_dict)
