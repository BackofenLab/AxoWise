
import nltk
import networkx as nx
from ie import InformationExtractor

text = "Monokine with inflammatory and chemokinetic properties. Binds to CCR1, CCR4 and CCR5. One of the major HIV-suppressive factors produced by CD8+ T-cells. Recombinant MIP-1-alpha induces a dose-dependent inhibition of different strains of HIV-1, HIV-2, and simian immunodeficiency virus (SIV)."

sentences = nltk.sent_tokenize(text)

extractor = InformationExtractor()

for sentence in sentences:
    print(sentence)
    dep_graph = extractor.dependency_graph(sentence)
    vis_graph = nx.nx_agraph.to_agraph(dep_graph)
    vis_graph.draw("dep_graph.png", prog = "dot")
    input()

extractor.clean_up()
