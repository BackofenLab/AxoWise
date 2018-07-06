
import os
import nltk
import networkx as nx
from nltk.parse.stanford import StanfordDependencyParser
from geniatagger import GENIATagger

os.environ['CLASSPATH'] = "stanford-parser-full-2018-02-27/"

class InformationExtractor:

    def __init__(self, tagger = GENIATagger(os.path.join(".", "geniatagger-3.0.2", "geniatagger"))):
        self.tagger = tagger
        self.dependency_parser = StanfordDependencyParser()

    def uncapitalize(self, string : str):
        if len(string) < 1:
            return string

        return string[: 1].lower() + string[ 1:]

    def is_abbreviation(self, word : str):
        for char in word:
            if not char.isalpha():
                continue
            if char.islower():
                return False

        return True

    def sentences(self, text : str):
        return nltk.sent_tokenize(text)

    def tag(self, sentence : str):
        return self.tagger.tag(self.uncapitalize(sentence))

    def chunkize(self, tagged_sentence):
        chunks = []
        current_chunk, current_tag = [], None
        for entry in tagged_sentence:
            word, base, pos_tag, chunk, named_entity = entry
            if chunk[0] == "B": # chunk opening
                if len(current_chunk) > 0:
                    chunk_str = " ".join(current_chunk)
                    chunks.append((chunk_str, current_tag))
                    current_chunk.clear()
                current_tag = chunk.split("-")[1]
                current_chunk.append(word)
            elif chunk[0] == "I": # chunk extension
                assert chunk.split("-")[1] == current_tag
                current_chunk.append(word)
            else: # not in a chunk
                if len(current_chunk) > 0:
                    chunk_str = " ".join(current_chunk)
                    chunks.append((chunk_str, current_tag))
                    current_chunk.clear()
                chunks.append((word, pos_tag))

        return chunks

    def dependency_graph(self, sentence : str):
        tagged = list(self.tag(sentence))
        tagged_reduced = list(map(lambda t: (t[0], t[2]), tagged))
        for i, (word, pos_tag) in enumerate(tagged_reduced):
            tagged_reduced[i] = ("{}-{}-{}".format(word, i, pos_tag), pos_tag)

        nltk_dep_graph = list(self.dependency_parser.tagged_parse(tagged_reduced))[0]
        graph = nx.MultiDiGraph()

        for first, relation, second in nltk_dep_graph.triples():
            graph.add_node(first[0], pos = first[1])
            graph.add_node(second[0], pos = second[1])
            graph.add_edge(second[0], first[0], label = relation)

        return graph

    def clean_up(self):
        self.tagger.stop()

