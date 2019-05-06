
import neomodel
from neomodel import (IntegerProperty, Relationship, RelationshipFrom,
                      RelationshipTo, StringProperty, StructuredNode,
                      UniqueIdProperty, db)

class Protein(StructuredNode):
    iid = IntegerProperty(index=True, required=True)
    external_id = StringProperty(required=True)
    name = StringProperty(required=True)
    description = StringProperty(required=True)
    species_id = IntegerProperty(required=True)

    association = Relationship("Protein", "ASSOCIATION")
    pw_in = RelationshipTo("Pathway", "IN")

class Pathway(StructuredNode):
    iid = IntegerProperty(index=True, required=True)
    name = StringProperty(required=True)
    description = StringProperty(required=True)
    species_id = IntegerProperty(required=True)

    p_in = RelationshipFrom("Protein", "IN")

class Disease:
    iid = IntegerProperty(index=True, required=True)
    name = StringProperty(required=True)

    pw_in = RelationshipTo("Pathway", "IN")

class Drug:
    iid = IntegerProperty(index=True, required=True)
    name = StringProperty(required=True)

    pw_in = RelationshipTo("Pathway", "IN")

class Compound:
    iid = IntegerProperty(index=True, required=True)
    name = StringProperty(required=True)

    pw_in = RelationshipTo("Pathway", "IN")

class Class:
    name = StringProperty(index=True, required=True)

    pw_in = RelationshipFrom("Pathway", "IN")
    c_in = RelationshipFrom("Class", "IN")
