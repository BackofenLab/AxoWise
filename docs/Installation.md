# Installation for Ubuntu

## Setting up the environment

To install the Protein Graph Database on Ubuntu, follow these steps:

1. Clone the repository. To access the repo, you need to add your SSH key to your GitHub account. Refer to
   this [guide](https://jdblischak.github.io/2014-09-18-chicago/novice/git/05-sshkeys.html) for more information.
   ```commandline
   git clone git@github.com:BackofenLab/protein-graph-database.git
   cd protein-graph-database/
   ```
2. Install the required software, including Anaconda, Java, and Neo4j. Refer to [Requirements.mk](../Requirements.mk)
   for details.
   ```commandline
   make requirements
   ```

3. Create the conda environment.
   ```commandline
   make env
   conda activate pgdb
   ```

## Dummy Data Setup

To automate the download of dummy data from Google Drive and the insertion into the database, follow these steps:

1. Run the following command to set up the dummy data:

   ```commandline
   make dummydata
   ```

Executing the above command will seamlessly handle the installation of the `gdown` tool, download the dummy data, and
insert it into the database.
`Gdown` is a helper tool to automate the download from Google Drive.

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

1. Create the file ```protein-graph-database/config.yml```
2. Insert the following content:
    ```yml
    # Neo4j Database Credentials
    neo4j:
      host: "localhost"
      port: 7687
      username: "neo4j"
      password: "pgdb"
   ```

## Installing and using ollama

1. Download and install ollama:
   ```commandline
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. Make sure ollama for python is installed:
    ```commandline
   pip install ollama
   ```
3. Start ollama as a system:
   ```commandline
   sudo systemctl start ollama
   ```
4. To check if ollama was correctly started and the gpu recognized check logs:
   ```commandline
   journalctl -e -u ollama
   ```
5. Add environmental variables (such as the one to keep the model alive and loaded in memory):
   ```commandline
   sudo systemctl edit ollama.service
   ```
   ```ini
   [Service]
   Environment="OLLAMA_KEEP_ALIVE=-1"
   ```
6. Restart ollama and reload systemd:
   ```commandline
   systemctl daemon-reload
   systemctl restart ollama
   ```
7. Soft start llama3 to keep in memory:
   ```commandline
   ollama run llama3 ""
   ```
8. Check if the model was correctly loaded and is using the gpu:
   ```commandline
   ollama ps
   ```
