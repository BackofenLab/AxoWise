---
title: Benchmark
category: papers
permalink: /benchmark
---

Paper: Huang et al., Systematic Evaluation of Molecular Networks for Discovery of Disease Genes, Cell Systems (2018),
https://doi.org/10.1016/j.cels.2018.03.001

## Introduction
- PathGuide website: over 700 pathway and molecular interaction databases available to the general public
- [Network Data Exchange (NDEx)](http://www.ndexbio.org/) - an attempt to provide a common public repository for biological network models of all types
- Benchmarks to aid in selecting the most appropriate networks for _a specific human disease_ or _molecular pathway of interest_
- Score of 21 popular human gene interaction networks by their ability to recover gene
sets that characterize a wide variety of diseases

## Results

# Databases
- Focusing on physical protein-protein interactions:
    - [Database for Interacting Proteins (DIP)](http://dip.mbi.ucla.edu/)
    - [Human Protein Reference Database (HPRD)](http://www.hprd.org/)
- Concatenating protein interactions from multiple molecular networks with many additional
interaction types (e.g. genetic interactions):
    - [ConsensusPathDB](http://cpdb.molgen.mpg.de)
    - MultiNet
- Quantitatively integrating different studies and interaction types into a _single integrated score_ for each gene pair based on the total weight of evidence:
    - [HumanNet](http://www.functionalnet.org/humannet/)
    - [Search Tool for Recurring Instances of Neighboring Genes (STRING)](https://string-db.org/)

# Benchmark
- Score how well each network is able to recover a diverse collection of disease-associated gene sets
- Each gene set was randomly split into two subsets
- Ability of one subset to recover the other within the network, using the technique of network propagation under the random walk with restart model
- Recovery was scored using the area under precision-recall curve (AUPRC)
- The average AUPRC over repeated trials was calibrated against a null distribution of AUPRC scores from networks in which individual edges had been shuffled, preserving node degrees
- Comparison with this null distribution allowed the AUPRC to be expressed as a Z score, henceforth called the network's "performance
score"
- Recovery of 446 disease-associated gene sets from the [DisGeNET](http://www.disgenet.org/) database

# Performance
- For recovery of these literature gene sets, we found that STRING had the best overall performance

![](https://preview.ibb.co/dNkueJ/benchmark1.png)

- Noticed that many of the larger networks appeared to be the best performing
- Examined how performance rankings change when correcting each network's performance for the number of interactions in the network:
    - The smallest network (DIP) moved to the top of the rankings, suggesting that, per edge, this network is most efficient

![](https://image.ibb.co/jWMpDd/benchmark2.png)

- Did not find any additional network properties, other than the size, that is significantly correlated with performance
- Testing literature bias:
    - Removed all interactions in STRING and HumanNet that were based solely on text mining
        - Found that filtering greatly reduced the performance of HumanNet
        - In contrast, such filtering did not greatly affect the performance of STRING
    - Evaluated all networks on gene sets that had been constructed independently of literature mining:
        - Found that [GeneMANIA](https://genemania.org/) and [GIANT (Genome-scale Integrated
Analysis of gene Networks in Tissues)](http://giant.princeton.edu/) were the best performing networks on these expression gene sets, with STRING
ranking third
- **Network integration**:
    - Created a series of composite networks of decreasing size
    - By requiring a minimum of two networks supporting each interaction, the performance was significantly improved over the best individual network (STRING) despite having a much smaller network size
     - This configuration was optimal, and we call this optimal configuration the "Parsimonious Composite Network" (PCNet)

# Discussion
- When studying a particular disease, one might start with the networks that performed best on that particular gene set, instead of or in addition to the networks that were the best performers overall
- We were able to derive a much smaller PCNet that outperformed a network twice its size: this suggests at least one straightforward method of contracting the size of a reference network without sacrificing performance - requiring multiple database support for interactions
