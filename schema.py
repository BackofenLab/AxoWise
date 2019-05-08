
import neomodel
from neomodel import (IntegerProperty, Relationship, RelationshipFrom,
                      RelationshipTo, StringProperty, StructuredNode,
                      UniqueIdProperty, One, OneOrMore, StructuredRel)

class Entity(StructuredNode):

    __abstract_node__ = True

    def __hash__(self):
        return hash(self.id)

class Association(StructuredRel):
        experiments = IntegerProperty(required=False)
        database = IntegerProperty(required=False)
        textmining = IntegerProperty(required=False)
        coexpression = IntegerProperty(required=False)
        neighborhood = IntegerProperty(required=False)
        fusion = IntegerProperty(required=False)
        cooccurence = IntegerProperty(required=False)
        combined_score = IntegerProperty(required=True, db_property="combined")

class Protein(Entity):
    id_ = IntegerProperty(unique_index=True, required=True, db_property="id")
    external_id = StringProperty(unique=True, required=True)
    name = StringProperty(index=True, required=True)
    description = StringProperty(required=True)
    species_id = IntegerProperty(required=True)

    associations = Relationship("Protein", "ASSOCIATION", model=Association)
    actions = Relationship("Protein", "ACTION")
    pathways = RelationshipTo("Pathway", "IN")

class Pathway(Entity):
    id_ = StringProperty(unique_index=True, required=True, db_property="id")
    name = StringProperty(index=True, required=True)
    description = StringProperty(required=True)
    species_id = IntegerProperty(required=True)

    proteins = RelationshipFrom("Protein", "IN")
    diseases = RelationshipFrom("Disease", "IN")
    drugs = RelationshipFrom("Drug", "IN")
    compounds = RelationshipFrom("Compound", "IN")
    cls = RelationshipTo("Class", "IN")

class Disease(Entity):
    id_ = StringProperty(unique_index=True, required=True, db_property="id")
    name = StringProperty(required=True)

    pathways = RelationshipTo("Pathway", "IN")

class Drug(Entity):
    id_ = StringProperty(unique_index=True, required=True, db_property="id")
    name = StringProperty(required=True)

    pathways = RelationshipTo("Pathway", "IN")

class Compound(Entity):
    id_ = StringProperty(unique_index=True, required=True, db_property="id")
    name = StringProperty(required=True)

    pathways = RelationshipTo("Pathway", "IN")

class Class(Entity):
    name = StringProperty(unique_index=True, required=True)

    pathways = RelationshipFrom("Pathway", "IN")
    parent = RelationshipTo("Class", "IN", cardinality=One)
    children = RelationshipFrom("Class", "IN", cardinality=OneOrMore)
