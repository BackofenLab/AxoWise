"""
A script containing the class that supports writing
dynamic networks to Gephi's Graph Exchange XML Format
(GEXF).
"""

import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

"""
[Dynamics]
The whole graph, each node, each edge and their respective data values
may have time limits, beginning with an XML-attribute `start` and ending
with `end`.
"""

class GEXF:

    _type_map = {
        int: "integer",
        float: "float",
        bool: "boolean",
        str: "string"
    }

    def __init__(self, path: str):
        self.path = path

        # Root element
        self.root = ET.Element(
            "gexf",
            # Schema
            # https://gephi.org/gexf/1.2draft/gexf-12draft-primer.pdf
            {
                "xmlns": "http://www.gexf.net/1.2draft",
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema−instance",
                "xsi:schemaLocation": "http://www.gexf.net/1.2drafthttp://www.gexf.net/1.2draft/gexf.xsd",
                "version": "1.2"
            }
        )

        # Meta info
        meta = ET.Element(
            "meta",
            lastmodifieddate=datetime.date.today().isoformat()
        )
        self.root.append(meta)

        # Graph
        graph = ET.Element("graph", mode="dynamic")
        self.root.append(graph)

        # Attributes
        self.node_attributes = ET.Element("attributes", {"class": "node"})
        graph.append(self.node_attributes)

        self.edge_attributes = ET.Element("attributes", {"class": "edge"})
        graph.append(self.edge_attributes)

        self._node_attr2id = dict()
        self._edge_attr2id = dict()

        # Nodes
        self.nodes = ET.Element("nodes")
        graph.append(self.nodes)

        # Edges
        self.edges = ET.Element("edges")
        graph.append(self.edges)

        self.tree = ET.ElementTree(self.root)
        self.graph = graph

    def save(self):
        # TODO: Pretty-print to a file
        self.tree.write(self.path, encoding="utf-8", xml_declaration=True)

    def _attributes_dict_to_elements(self, attributes: dict):
        # TODO: Support default attribute values
        for id, (title, type) in enumerate(attributes.items()):
            xmltype = GEXF._type_map.get(type, None)
            if xmltype is None:
                raise ValueError(f"An attribute cannot be of type {type}!")
            yield ET.Element("attribute", id=str(id), title=title, type=xmltype)

    def set_node_attributes(self, **attrs):
        for attribute in self._attributes_dict_to_elements(attrs):
            id, title = attribute.get("id"), attribute.get("title")
            self._node_attr2id[title] = id
            self.node_attributes.append(attribute)

    def set_edge_attributes(self, **attrs):
        for attribute in self._attributes_dict_to_elements(attrs):
            id, title = attribute.get("id"), attribute.get("title")
            self._edge_attr2id[title] = id
            self.edge_attributes.append(attribute)

    def add_node(self, id: str, label: str, **attrs):
        node = ET.Element("node", id=id, label=label)
        attvalues = ET.Element("attvalues")
        node.append(attvalues)

        for title, value in attrs.items():
            id = self._node_attr2id.get(title, None)
            if id is None:
                raise ValueError(f"Attribute {title} not set before adding nodes!")

            attvalue = ET.Element("attvalue", {
                "for": id, "value": str(value)
            })
            attvalues.append(attvalue)

        self.nodes.append(node)

    def add_edge(self, source: str, target: str, **attrs):
        edge = ET.Element("edge", source=source, target=target)
        attvalues = ET.Element("attvalues")
        edge.append(attvalues)

        for title, value in attrs.items():
            id = self._edge_attr2id.get(title, None)
            if id is None:
                raise ValueError(f"Attribute {title} not set before adding edges!")

            attvalue = ET.Element("attvalue", {
                "for": id, "value": str(value)
            })
            attvalues.append(attvalue)

        self.edges.append(edge)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

if __name__ == "__main__":

    with GEXF("test.gexf") as gexf:
        gexf.set_node_attributes(
            description=str
        )
        gexf.set_edge_attributes(
            score=float
        )

        # TODO Support `start` and `end` keys
        gexf.add_node("1", "CCR5", description="Receptor")
        gexf.add_node("2", "CCL5", description="Ligand")
        gexf.add_edge("1", "2", score=0.9)
