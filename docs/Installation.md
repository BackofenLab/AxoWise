# Installation for Ubuntu

## Setting up the environment
To install the Protein Graph Database on Ubuntu, follow these steps:

1. Clone the repository. To access the repo, you need to add your SSH key to your GitHub account. Refer to this [guide](https://jdblischak.github.io/2014-09-18-chicago/novice/git/05-sshkeys.html) for more information.
   ```commandline
   git clone git@github.com:BackofenLab/protein-graph-database.git
   cd protein-graph-database/
   ```
2. Install the required software, including Anaconda, Java, and Neo4j. Refer to [Requirements.mk](../Requirements.mk) for details.
   ```commandline
   make requirements
   ```

3. Create the conda environment.
   ```commandline
   make env
   conda activate pgdb
   ```

## Set up Dummy-Data
To set up the dummy-data, follow these steps:

1. Download the [test sample database](https://drive.google.com/file/d/1S8_O2HCeMKwukwnTHlFmf1KLQnbfcXAN/view) to your Downloads folder.
2. Load the dump file into your own database.
   ```commandline
   sudo neo4j-admin load --from=$HOME/Downloads/newmouse2db.dump --database=neo4j --force
   ```

## Create a Neo4J Account
To create a Neo4j account, follow these steps:

1. Start Neo4j with the following command:
   ```commandline
   make neo4j
   ```
2. Open [localhost:7474](http://localhost:7474/browser/) in your web browser.
   - Login with the following credentials:
     - Username: neo4j
     - Password: neo4j
   - Change the password to: pgdb.

## Set Credentials
1. Create the file ```protein-graph-database/credentials.yml```
2. Insert the following content:
    ```yml
   # Neo4j Database Credentials
   neo4j:
       host: "localhost"
       port: 7687
       pw: "pgdb"
   ```
