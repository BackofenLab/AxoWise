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
        self.node_attributes = ET.Element("attributes", {"class": "node", "mode": "dynamic"})
        graph.append(self.node_attributes)

        self.edge_attributes = ET.Element("attributes", {"class": "edge", "mode": "dynamic"})
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

    def add_node(self, id: str, label: str, start=None, end=None, **attrs):
        kwargs = dict(id=id, label=label)
        if start is not None:
            kwargs["start"] = str(start)
        if end is not None:
            kwargs["end"] = str(end)
        node = ET.Element("node", **kwargs)
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

    def add_edge(self, source: str, target: str, start=None, end=None, **attrs):
        kwargs = dict(source=source, target=target)
        if start is not None:
            kwargs["start"] = str(start)
        if end is not None:
            kwargs["end"] = str(end)
        edge = ET.Element("edge", **kwargs)
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

    def _find_node(self, node_id):
        return self.nodes.find(f"./node[@id='{node_id}']")

    def _find_edge(self, source, target):
        return self.edges.find(f"./edge[@source='{source}'][@target='{target}']")

    def set_dynamic_node_attribute(self, node_id, title, value, start, end):
        # Find node
        node = self._find_node(node_id)
        if node is None:
            raise ValueError(f"Node {node_id} does not exist!")

        # Find attvalues
        attvalues = node.find("./attvalues")

        # Add the attribute
        id = self._node_attr2id.get(title, None)
        if id is None:
            raise ValueError(f"Attribute {title} not set before adding nodes!")

        attvalue = ET.Element("attvalue", {
            "for": id,
            "value": str(value),
            "start": str(start),
            "end": str(end)
        })
        attvalues.append(attvalue)

    def set_dynamic_edge_attribute(self, source, target, title, value, start, end):
        # Find edge
        edge = self._find_edge(source, target)
        if edge is None:
            raise ValueError(f"Edge connecting nodes {source} and {target} does not exist!")

        # Find attvalues
        attvalues = edge.find("./attvalues")

        # Add the attribute
        id = self._edge_attr2id.get(title, None)
        if id is None:
            raise ValueError(f"Attribute {title} not set before adding edges!")

        attvalue = ET.Element("attvalue", {
            "for": id,
            "value": str(value),
            "start": str(start),
            "end": str(end)
        })
        attvalues.append(attvalue)

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

        gexf.add_node("1", "CCR5", start=0, end=10, description="Receptor")
        gexf.add_node("2", "CCL5", start=0, end=10, description="Ligand")
        gexf.add_edge("1", "2", start=3, end=7)
