from xml.etree import ElementTree
import url

P51681 = url.get("http://www.uniprot.org/uniprot/P51681.xml") # CCR5_HUMAN
root = ElementTree.fromstring(P51681)

xml_namespace = dict(
    ns = "http://uniprot.org/uniprot"
)

primary_name = root.find("./ns:entry/ns:gene/ns:name[@type='primary']", xml_namespace).text
print("Primary name:", primary_name)
