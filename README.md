# BioNetViz

BioNetViz is a web service that utilizes an integrated graph system to visualize biological entities, functional terms, and publications. It emphasizes the visualization and interaction between different graph systems, providing convenient usability for exploring biological communities. Users can easily access information derived from graphs of functional terms and publications for functional exploration.

Currently, BioNetViz supports the functional exploration of protein graphs. Future plans include integrating various types of biological entities.

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
