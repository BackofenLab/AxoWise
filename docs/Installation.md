# Installation

### Requirements
- [Anaconda](https://conda.io/en/latest/) 
- [npm/Node.js](https://nodejs.org/en/download) 
- [Java (version 8! because of neo4j 4.4)](https://adoptium.net/de/temurin/archive/?version=8)
- [Maven](https://maven.apache.org/download.cgi) 
- [Neo4j (version 4.4!)](https://neo4j.com/download-center/) 
  - [APOC (version 4.4!)](https://neo4j.com/labs/apoc/4.4/installation/)

### Setting up the environment
1. clone the repository
   ```commandline
   git clone https://github.com/BackofenLab/protein-graph-database.git
   cd protein-graph-database/
   ```
2. create the conda environment
   ```commandline
   make env
   conda activate pgdb
   ```

### Setting up the Database
1. download [test sample database](https://drive.google.com/file/d/1S8_O2HCeMKwukwnTHlFmf1KLQnbfcXAN/view)
2. stop the neo4j database if running
   ```commandline
   stop neo4j
   ```
3. load the dump file into your own database
   ````commandline
   neo4j-admin load --from=<backup-directory> --database=<database-name> --forc
   ````
4. start neo4j
   ````commandline
   start neo4j
   ````
   or
   ````commandline
   neo4j console
   ````

### Install APOC Plugin
1. move the Apoc.jar into neo4j/plugin
2. add following permissions to the neo4j.config
   ````commandline
   dbms.security.procedures.whitelist=apoc.export.*
   apoc.import.file.use_neo4j_config=false
   apoc.export.file.enabled=true
   ````
