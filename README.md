# AxoWise

AxoWise is a web service tool engineered to convert complex networks of knowledge into contextual insights through interactive visualization and AI techniques.

## Motivation

> "Knowledge is the first concern of the scientist, but wisdom is the ultimate intellectual goal of us all." — *The Stress of Life*, Hans Selye, p. 404.

AxoWise is designed around the theme of "Bridging Knowledge and Wisdom through Networks." Inspired by the adaptability and regenerative capabilities of the axolotl, the tool symbolizes the transformation of isolated data points into interconnected, contextual insights. Just as the axolotl adapts and regenerates, AxoWise adapts to diverse layers of knowledge—such as biological networks, networks of functional terms, and networks of publications—integrating them into a cohesive whole. This process of connecting and integrating fragmented data points within their relevant contexts enables the discovery of holistic insights, much like how the brain’s neural pathways create complex understanding through their interconnectedness.

## Current Status

Currently, AxoWise supports biological networks by integrating protein networks along with networks of functional terms and publication abstracts. These interconnected layers of knowledge provide a robust foundation for exploring the interactions and functions within biological systems, delivering contextual insights. In the next phase of development, we aim to expand AxoWise by incorporating regulatory networks, which are crucial for understanding gene regulation and cellular processes. By adding regulatory network data, AxoWise will further enhance its ability to reveal complex interactions, such as transcriptional regulation and signaling pathways, offering users a deeper and more contextualized view of biological networks.





## Project Structure
The Protein Graph Database is organized into several directories:

- [docs](docs) contains files used for documentation, including images or text files.
- [backend/src](backend/src) contains the [Flask](https://flask.palletsprojects.com/en/2.2.x/) server code,
  which serves all files and handles requests to the database.
- [backend/gephi](backend/gephi) contains the code to pre-organize the data into nodes,
  which can then be used in the frontend. It is used as a submodule in the server.
- [backend/test_data](backend/test_data) contains test data.
- [frontend](frontend) contains the [Vue](https://vuejs.org/) frontend code used to visualize the protein data.
- [scrapting/KEGG](scraping/KEGG) contains the code used to fetch data from the KEGG source. This directory is only used as a reference for future scraping.
## How to Use
To use the Protein Graph Database, follow these steps:

1. Follow the [Installation Guide](docs/Installation.md)
2. Run the project by executing the following commands:
   1. ```make neo4j``` (starts Neo4J database)
   2. ```conda activate pgdb``` (activates the conda environment)
   3. ```make build``` (builds the entire project)
   4. ```make start``` (runs the project)
