# Installation for Ubuntu

### Setting up the environment
1. clone the repository. To access the repo, you need to add SSH key to your GitHub account. Here is the [guide](https://jdblischak.github.io/2014-09-18-chicago/novice/git/05-sshkeys.html).
   ```commandline
   git clone git@github.com:BackofenLab/protein-graph-database.git
   cd protein-graph-database/
   ```

2. install needed software (java, maven,...)
   ```commandline
   cd docs/installation
   make all
   ```

2. create the conda environment
   ```commandline
   make env
   conda activate pgdb
   ```

### Set up Dummy-Data
1. download [test sample database](https://drive.google.com/file/d/1S8_O2HCeMKwukwnTHlFmf1KLQnbfcXAN/view)
2. load the dump file into your own database
   ````commandline
   sudo neo4j-admin load --from=$HOME/Downloads/newmouse2db.dump --database=neo4j --force
   ````

### Create Neo4J Account
1. start neo4j with ````make neo4j````
2. open [localhost:7474](http://localhost:7474/browser/)
   - login with user:
     - name: neo4j
     - pw: neo4j
   - change password to: pgdb
