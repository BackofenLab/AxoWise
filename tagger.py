import subprocess
import re
import os

class GeniaTagger:

    def __init__(self, executable_rel_path):
        self.executable_rel_path = executable_rel_path

    def tag(self, text : str):
        p = subprocess.run(os.path.join(os.getcwd(), self.executable_rel_path, "geniatagger"), input = text.encode("utf-8"), stdout = subprocess.PIPE, cwd = self.executable_rel_path)
        lines = p.stdout.decode("utf-8").split("\n")
        for line in lines:
            row = tuple(re.split("\t+", line))
            if len(row) == 5: # Word, Base Form, Part-Of-Speech, Chunk, Named Entity 
                yield (row[0], row[2])

if __name__ == "__main__":
    tagger = GeniaTagger("./geniatagger-3.0.2/")
    for t in tagger.tag("Monokine with inflammatory and chemokinetic properties. Binds to CCR1, CCR4 and CCR5. One of the major HIV-suppressive factors produced by CD8+ T-cells. Recombinant MIP-1-alpha induces a dose-dependent inhibition of different strains of HIV-1, HIV-2, and simian immunodeficiency virus (SIV)."):
        print(t)