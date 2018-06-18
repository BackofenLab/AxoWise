
import os

os.environ['CLASSPATH'] = "stanford-parser-full-2018-02-27/:stanford-corenlp-full-2018-02-27/"

from nltk.parse.stanford import StanfordParser
import nltk
# nltk.download("punkt")
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

from tagger import GeniaTagger

parser = StanfordParser()
tagger = GeniaTagger("./geniatagger-3.0.2/")

def tree_has_labeled_children(tree, label):
    ret = False
    for subtree in tree:
        if type(subtree) != nltk.tree.Tree:
                continue
        if subtree.label() == label:
            return True
        else:
            ret = ret or tree_has_labeled_children(subtree, label)
    return ret

def last_labeled(tree, label):
    valid = []
    for subtree in tree:
        if type(subtree) != nltk.tree.Tree:
                continue
        if subtree.label() == label and not tree_has_labeled_children(subtree, label):
            valid.append(subtree.leaves())
        else:
            valid += last_labeled(subtree, label)
    return valid

uncapitalize = lambda s: s[:1].lower() + s[1:] if s else ''

text = "Monokine with inflammatory and chemokinetic properties. Binds to CCR1, CCR4 and CCR5. One of the major HIV-suppressive factors produced by CD8+ T-cells. Recombinant MIP-1-alpha induces a dose-dependent inhibition of different strains of HIV-1, HIV-2, and simian immunodeficiency virus (SIV)."

sentences = nltk.sent_tokenize(text)

subject = "CCR5"

for i, sentence in enumerate(sentences):

    print("------------ Sentece {} ------------".format(i + 1))

    tagged = list(tagger.tag(sentence))

    trees = list(parser.tagged_parse(tagged))
    tree = trees[0]
    print(len(trees), "trees")

    if len(tree) == 1 and tree[0].label() == "NP": # Subject --IS--> ...
        print(subject, " -> ", " ".join(tree.leaves()))
    else:
        print("Noun phrases")
        for np in last_labeled(tree, "NP"):
            print(" ".join(np))

    print("Verb phrases:")
    for vp in last_labeled(tree, "VP"):
        print(" ".join(vp))

    tree.draw()
