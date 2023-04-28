# Protein Graph Database

## How to install?
A guid is given [here](docs/Installation.md).

## Project Structure
- [docs](docs) contains files used for documentation including images or text-files.
- [backend/src](backend/src) contains the [Flask](https://flask.palletsprojects.com/en/2.2.x/) server code used to serve all 
  files and handle requests to the database.
- [backend/gephi](backend/gephi) contains code to preorganize the data in nodes.
  These preorganized nodes can then be used in the frontend.
  It is used as a submodule in the server.
- [frontend](frontend) contains the [Vue](https://vuejs.org/) frontend code to visualize the protein-data.
- [scrapting/KEGG](scraping/KEGG) contains code to fetch data from the KEGG source.
  This dir is only used as a reference for future scraping.

## How to Use?
0. ask someone for the "credentials.yml" file
1. build
   ````commandline
   ./scripts/build.sh
   ````
3. run
   ````commandline
   ./scripts/run.sh
   ````
   
