# Installation

_Hint: if installing on Ubuntu check-out [these versions](ubuntu-versions.txt)!_

### Requirements
- [Anaconda](https://conda.io/en/latest/) 
- [npm/Node.js (Version 18 because of Sigma)](https://nodejs.org/en/download)
- [Java (version 8! because of neo4j 4.4)](https://adoptium.net/de/temurin/archive/?version=8)
- [Maven](https://maven.apache.org/download.cgi) 
- [Neo4j (version 4.4!)](https://neo4j.com/download-center/) 
  - [APOC-core (version 4.4!)](https://neo4j.com/labs/apoc/4.4/installation/) [(direct download)](https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/4.4.0.1)

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
### Install APOC Plugin
1. move the Apoc.jar into neo4j/plugin
2. add following permissions to the neo4j.config
   ````commandline
   dbms.security.procedures.whitelist=apoc.export.*
   apoc.import.file.use_neo4j_config=false
   apoc.export.file.enabled=true
   ````

### Set up Dummy-Data
1. download [test sample database](https://drive.google.com/file/d/1S8_O2HCeMKwukwnTHlFmf1KLQnbfcXAN/view)
2. stop the neo4j database if running
   ```commandline
   stop neo4j
   ```
3. load the dump file into your own database
   ````commandline
   neo4j-admin load --from=<backup-directory> --database=<database-name> --forc
   ````

### Create Neo4J Account
1. start neo4j with ````start neo4j````or ````neo4j console````
2. open [localhost:7474](http://localhost:7474/browser/)
   - login with user:
     - name: neo4j 
     - pw: neo4j
   - change password to: pgdb
