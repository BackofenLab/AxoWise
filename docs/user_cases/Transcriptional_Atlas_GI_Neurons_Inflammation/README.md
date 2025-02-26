# Protein Network Analysis for the Transcriptional Atlas of Gastrointestinal (GI) Neurons During Inflammation

## Purpose

This repository supports the **protein network analysis** component of the **Transcriptional Atlas of Gastrointestinal (GI) Neurons During Inflammation**. The goal is to uncover molecular interactions and biological pathways that drive the inflammatory response in GI neurons. By integrating protein-protein interactions with transcriptional data, we aim to identify functional modules and gain deeper insights into neuroinflammation.

## Features

- **Protein Interaction Network Construction**: Builds networks using curated protein-protein interaction databases specific to GI neuron inflammation.
- **Functional Module Identification**: Detects biologically meaningful clusters of interacting proteins affected by inflammation.
- **Pathway and Ontology Enrichment**: Maps protein modules to known signaling pathways and gene ontology (GO) terms relevant to GI neuroinflammation.
- **Reproducible and Customizable Analysis**: Supports transcriptomics-integrated analysis with customizable input protein lists for tailored network exploration.

## How to Get Started

Follow these steps to perform protein network analysis using this repository:

1. **Prepare Input Data**: Use the provided dataset containing protein symbols or ENSEMBL IDs with their respective differential expression values. See the [project dataset](exp_DE_sigfy.csv) used in this study.
2. **Construct the Protein Network**: Generate an interaction network based on curated databases.
3. **Analyze Functional Modules**: Detect and visualize protein clusters.
4. **Perform Pathway Enrichment**: Identify biological pathways associated with functional modules.
5. **Save and Export Results**: Store network structures and findings for further research and publication. You can download the **project network structure file** [here](protein_interaction_DE_P1e-3_1.json), which represents the analyzed protein interactions in this study.

## Documentation and Further Resources

For detailed instructions on installation, analysis workflows, and dataset usage, explore the **user guide** and **use case examples** in the **[AxoWise GitHub Repository](https://github.com/BackofenLab/AxoWise)**.
