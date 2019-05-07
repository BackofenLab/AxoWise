
import neomodel
from neomodel import (IntegerProperty, Relationship, RelationshipFrom,
                      RelationshipTo, StringProperty, StructuredNode,
                      UniqueIdProperty)

class Protein(StructuredNode):
    iid = IntegerProperty(index=True, required=True)
    external_id = StringProperty(required=True)
    name = StringProperty(required=True)
    description = StringProperty(required=True)
    species_id = IntegerProperty(required=True)

    associations = Relationship("Protein", "ASSOCIATION")
    pathways = RelationshipTo("Pathway", "IN")

class Pathway(StructuredNode):
    iid = IntegerProperty(index=True, required=True)
    name = StringProperty(required=True)
    description = StringProperty(required=True)
    species_id = IntegerProperty(required=True)

    proteins = RelationshipFrom("Protein", "IN")

class Disease(StructuredNode):
    iid = IntegerProperty(index=True, required=True)
    name = StringProperty(required=True)

    pathways = RelationshipTo("Pathway", "IN")

class Drug(StructuredNode):
    iid = IntegerProperty(index=True, required=True)
    name = StringProperty(required=True)

    pathways = RelationshipTo("Pathway", "IN")

class Compound(StructuredNode):
    iid = IntegerProperty(index=True, required=True)
    name = StringProperty(required=True)

    pathways = RelationshipTo("Pathway", "IN")

class Class(StructuredNode):
    name = StringProperty(index=True, required=True)

    pathways = RelationshipFrom("Pathway", "IN")
    parent = RelationshipTo("Class", "IN")
    children = RelationshipFrom("Class", "IN")
