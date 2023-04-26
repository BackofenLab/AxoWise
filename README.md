# Protein Graph Database

## How to install?
A guid is given [here](docs/Installation.md).

## Project Structure
- [docs](docs) contains files used for documentation including images or text-files. 
  All files are referenced from this Readme!
- [frontend](frontend) contains the [Vue](https://vuejs.org/) frontend code to visualize the protein-data.
- [backend/server](backend/server) contains the [Flask](https://flask.palletsprojects.com/en/2.2.x/) server code used to serve all 
  files and handle requests to the database.
- [backend/gephi](backend/gephi) contains code to preorganize the data in nodes.
  These preorganized nodes can then be used in the frontend.
  It is used as a submodule in the server.
- [fetching/KEGG](fetching/KEGG) contains code to fetch data from the KEGG source.
  This dir is only used as a reference for future fetching.

## Run
1. build frontend
   ````commandline
   cd frontend/
   npm install
   npm run build
   ````
2. build backend
   ````commandline
   cd database/gephi-backend
   mvn install
   ````
3. run
   ````commandline
   python backend/server.py
   ````
   
