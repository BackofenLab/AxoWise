
import neomodel
from neomodel import (IntegerProperty, Relationship, RelationshipFrom,
                      RelationshipTo, StringProperty, StructuredNode,
                      UniqueIdProperty, One, OneOrMore)

class Protein(StructuredNode):
    iid = IntegerProperty(unique_index=True, required=True)
    external_id = StringProperty(unique=True, required=True)
    name = StringProperty(index=True, required=True)
    description = StringProperty(required=True)
    species_id = IntegerProperty(required=True)

    associations = Relationship("Protein", "ASSOCIATION")
    actions = Relationship("Protein", "ACTION")
    pathways = RelationshipTo("Pathway", "IN")

class Pathway(StructuredNode):
    iid = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(index=True, required=True)
    description = StringProperty(required=True)
    species_id = IntegerProperty(required=True)

    proteins = RelationshipFrom("Protein", "IN")
    diseases = RelationshipFrom("Disease", "IN")
    drugs = RelationshipFrom("Drug", "IN")
    compounds = RelationshipFrom("Compound", "IN")
    cls = RelationshipTo("Class", "IN", cardinality=One)

class Disease(StructuredNode):
    iid = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(required=True)

    pathways = RelationshipTo("Pathway", "IN")

class Drug(StructuredNode):
    iid = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(required=True)

    pathways = RelationshipTo("Pathway", "IN")

class Compound(StructuredNode):
    iid = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(required=True)

    pathways = RelationshipTo("Pathway", "IN")

class Class(StructuredNode):
    name = StringProperty(unique_index=True, required=True)

    pathways = RelationshipFrom("Pathway", "IN")
    parent = RelationshipTo("Class", "IN", cardinality=One)
    children = RelationshipFrom("Class", "IN", cardinality=OneOrMore)
