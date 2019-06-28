---
title: Documentation
category: notebooks
permalink: /documentation
---

[Prerequisites](#prerequisites)  
[Setting up the environment](#setting-up-the-environment)  
[Running unit tests](#running-unit-tests)  
[Downloading KEGG data for a certain species](#downloading-kegg-data-for-a-certain-species)  
[Building a Neo4j graph database](#building-a-neo4j-graph-database)  
[Running the server](#running-the-server)  
[Building the Docker container(s)](#building-the-docker-containers)  
[Starting the latest deployed Docker container(s)](#starting-the-latest-deployed-docker-containers)  
[Querying the Neo4j database](#querying-the-neo4j-database)

<br/>
<hr/>
<br/>

## Prerequisites
- [conda](https://conda.io/docs/) installed
- [PostgreSQL](https://www.postgresql.org/) server instance running (with the [STRING schema dumps](index#1-collect-the-data) loaded)
- [Neo4j](https://neo4j.com/) server instance running

## Setting up the environment
1. Clone the GitHub repository

    ```sh
    git clone https://github.com/BackofenLab/protein-graph-database.git
    cd protein-graph-database/
    ```

2. Create a conda environment ([environment.yml](https://github.com/BackofenLab/protein-graph-database/blob/master/environment.yml))

    ```sh
    make env
    ```

3. Activate the conda environment

    ```sh
    conda activate pgdb
    ```

## Running unit tests

Unit tests assume the following local configuration:
- Authentication mode for PostgreSQL user _postgres_ is set to _trust_
(in **pg_hba.conf**; read more [here](https://www.postgresql.org/docs/9.6/static/auth-pg-hba-conf.html))

    ```
    make test
    ```

## Downloading KEGG data for a certain species

Currently, only the KEGG data for human (_Homo sapiens_) and mouse (_Mus musculus_) is available in the project repository (_KEGG / data_). To add another species data, use the following steps:

1. Change the working directory to _KEGG /_

    ```sh
    cd KEGG/
    ```

2. Run the download script:

    ```sh
    python download.py species_name
    ```

    Positional arguments:

    ```sh
    species_name  Species name (e.g. Homo sapiens / human)
    ```

<p style="color: red;">When specifying the species name, please be as precise as possible. Otherwise, the scripts may yield an unwanted result. Fuzzy search is still not perfect.</p>

# Example:

To download KEGG data for chimpanzee (_Pan troglodytes_), run the following command:

```sh
python download.py --species_name "chimpanzee"
```

Output:
```
Downloading KEGG data for Pan troglodytes (chimpanzee).
Downloading pathways for: ptr
[1 / 326] Glycolysis / Gluconeogenesis
    Genes: 69
    10 gene(s) could not be mapped to STRING external ID!
[2 / 326] Citrate cycle (TCA cycle)
    Genes: 30
    4 gene(s) could not be mapped to STRING external ID!
[3 / 326] Pentose phosphate pathway
    Genes: 30
    9 gene(s) could not be mapped to STRING external ID!
...
```

## Building a Neo4j graph database
1. Provide credentials for accessing the databases

    - Create **credentials.yml** file in the root directory of the cloned repository. The format should be the following:

        ```yaml
        # PostgreSQL Database Credentials
        postgres:
            host: <hostname>
            port: <port>
            database: <database name>
            user: <username>
            pw: <password>

        # Neo4j Database Credentials
        neo4j:
            host: <hostname>
            port: <port>
            pw: <password>
        ```
    One credentials file is already available for tesing at _test/credentials.test.yml_.

2. Run the Python script (**build_graph_db.py**)

    ```sh
    python build_graph_db.py
    ```

    Available arguments:

    ```sh
    --credentials CREDENTIALS
                            Path to the credentials YAML file that will be used
                            (default: credentials.yml)
    --species_name SPECIES_NAME
                            Species name (default: Homo sapiens)
    --protein_list PROTEIN_LIST
                            Path to the file containing protein Ensembl IDs
                            (default: None)
    --combined_score_threshold COMBINED_SCORE_THRESHOLD
                            Threshold above which the associations between
                            proteins will be considered (default: None)
    --skip_actions SKIP_ACTIONS
                            Do not add protein - protein actions to the resulting
                            graph database (default: True)
    --skip_drugs SKIP_DRUGS
                            Do not add drugs to the resulting graph database
                            (default: False)
    --skip_compounds SKIP_COMPOUNDS
                            Do not add compounds to the resulting graph database
                            (default: False)
    --skip_diseases SKIP_DISEASES
                            Do not add diseases to the resulting graph database
                            (default: False)
    --keep_old_database KEEP_OLD_DATABASE
                            Do not overwrite the existing Neo4j graph database
                            (default: False)
    ```

# Example:

The following command builds a Neo4j database out of the mouse proteins and associations between them that have the combined score greater than 0.750.

```sh
python build_graph_db.py --credentials test/credentials.test.yml \
                       --species_name "mus musculus" \
                       --combined_score_threshold 750
```

Output:
```sh
Cleaning the old data from Neo4j database...
Creating compounds...
3460
Creating diseases...
0
Creating drugs...
0
Creating classes and class hierarchy...
43
Creating pathways and connecting them to classes...
326
Connecting compounds and pathways...
5984
Connecting diseases and pathways...
326
Connecting drugs and pathways...
326
Creating proteins...
22668
Creating protein - protein associations...
1322
Creating protein - protein actions...
0
Connecting proteins and pathways...
27750
Done!
```

## Running the server

Starting a server that exposes a REST API and serves the frontend files is as easy as running:
```sh
python server.py
```
The output should resemble the following:
```
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 ...

```

The server can then be accessed locally @ [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

<p style="color: red;">This is a development server, and it is not by any means ready to be used in production.</p>

## Building the Docker container(s)

- Neo4j server

    Requires [neo4j.human.mouse.400.dump](https://github.com/BackofenLab/protein-graph-database/releases/download/0.2/neo4j.human.mouse.400.dump) and [graph-algorithms-algo-3.5.3.3.jar](https://github.com/BackofenLab/protein-graph-database/releases/download/0.2/graph-algorithms-algo-3.5.3.3.jar) in the root directory of the Git repository.

    ```sh
    docker build -f docker/web/Dockerfile -t <repository>/pgdb-database:<version> .
    ```

- Web application
    ```sh
    docker build -f docker/database/Dockerfile -t <repository>/pgdb-web:<version> .
    ```

## Starting the latest deployed Docker container(s)

Definition of image names and how they are connected can be found in [docker-compose.yml](https://github.com/BackofenLab/protein-graph-database/blob/master/docker-compose.yml).

Make sure that you have `docker` and `docker-compose` installed. For Debian-based distributions, they are available via APT:

```bash
sudo apt install docker.io docker-compose
```

Database and server can be started running the following command in the root directory of our repository:

```bash
docker-compose up
```

The web application is accessible @ [http://localhost:5000/](http://localhost:5000/1)

After exiting, it is also recommended to clean up:

```bash
docker-compose down
```

## Querying the Neo4j database

# Command line interface (CLI)

Our Neo4j command line interface (CLI) is available in the form of a Python script.

```sh
usage: ./pgdb-cli [-h] [-i] [--name NAME]

optional arguments:
  -h, --help   show this help message and exit
  -i           Run the CLI in the interactive mode
  --name NAME  Name under which the batch results will be saved
```

`-i` flag starts CLI in the interactive mode. Otherwise, it expects a batch of queries from the standard input, separated by a newline (`\n`).

`--name` represents a directory name that will be created for storing the results. If not provided, the script generates its own name in a form of a timestamp.

**Interactive mode**

```sh
./pgdb-cli -i
```

Prompt (waiting for a query from the standard input):

```bash
=== Protein Graph Database CLI ===
>
```

After a query is typed in, one should press `Ctrl+D` (EOF) to send the query to the Neo4j database.

**Batch mode**

Example:

- queries.txt

    ```txt
    MATCH (source:Protein {species_id: 9606})-[a:ASSOCIATION]->(target:Protein)
    RETURN source, target, a.combined AS score

    MATCH (:Pathway {name: "Chemokine signaling pathway"})<-[:IN]-(drug:Drug)
    RETURN drug
    ```
- Command line usage

    ```sh
    cat queries.txt | ./pgbd-cli --name "best_queries_ever"
    ```

# Cypher queries

Make sure you are already familiar and comfortable with [Cypher and its syntax](https://neo4j.com/developer/cypher-query-language/).

Queries in this section use `name` property for matching since it is more convenient for a user. In order to match the nodes unambiguously, one should use `id` property instead.

Usually there are multiple nodes matching a given name. That is the reason we use fuzzy search and give a user the final decision.

Keeping [our database graph scheme](graph-db-scheme) in mind, queries are more or less straightforward and intuitive. The following examples cover various scenarios and should be enough to start writing basic to intermediate queries.

# Postprocessing

The Neo4j CLI contains a handful of postprocessing functions. These functions automatically split the returned data into separate tables (i.e. pandas DataFrames) suitable for writing to a CSV file. Other data formats are put into a single table as they are.

For each output table, the user is prompted whether she/he wants to save the table.

Currently, the following postprocessing is supported:

**Protein interactions**
- Expected RETURN format

    | Column name | Type    |
    | ----------- | ------- |
    | source      | Protein |
    | target      | Protein |
    | score       | number (representing the strength of the interaction) |

- Output tables:

    | nodes       |
    | ----------- |
    | id          |
    | external_id |
    | name        |
    | description |
    | species_id  |

    | edges       |
    | ----------- |
    | source      |
    | target      |
    | score       |

- Example:

    Best scoring 100 proteins associated with CCL5

    ```
    WITH "CCL5" as protein_name
    MATCH (source:Protein {name: protein_name})-[a:ASSOCIATION]-(target:Protein)
    RETURN source, a.combined AS score, target
    ORDER BY score DESC
    LIMIT 100
    ```

    ```
    [nodes]
         id               external_id    name                                        description species_id
    1847396      9606.ENSP00000293272    CCL5  Chemokine (C-C motif) ligand 5; Chemoattractan...       9606
    1847342      9606.ENSP00000292303    CCR5  Chemokine (C-C motif) receptor 5 (gene/pseudog...       9606
    2100220  10090.ENSMUSP00000039600    CCL5  Chemokine (C-C motif) ligand 5; Chemoattractan...      10090
    2101692  10090.ENSMUSP00000047646  CXCL10  Chemokine (C-X-C motif) ligand 10; In addition...      10090
    1848754      9606.ENSP00000305651  CXCL10  Chemokine (C-X-C motif) ligand 10; Chemotactic...       9606
    ...

    [edges]
     source   target score
    1847396  1847342   997
    2100220  2101692   995
    1847396  1848754   994
    1847396  1848852   994
    1847396  1862185   994
    ...
    ```

**Proteins**

- Expected RETURN format

    | Column name | Type    |
    | ----------- | ------- |
    | protein     | Protein |

- Output tables:

    | nodes       |
    | ----------- |
    | id          |
    | external_id |
    | name        |
    | description |
    | species_id  |

- Example:

    Proteins in Chemokine signaling pathway (for mouse)

    ```
    WITH "Chemokine signaling pathway" as pathway_name,
    10090 as species_id
    MATCH (:Pathway {
        name: pathway_name,
        species_id: species_id
    }
    )<-[:IN]-(protein:Protein)
    RETURN protein
    ```

    ```
    [nodes]
         id               external_id    name                                        description species_id
    2111516  10090.ENSMUSP00000106906    NCF1  Neutrophil cytosolic factor 1; NCF2, NCF1, and...      10090
    2098897  10090.ENSMUSP00000033827    GRK1  G protein-coupled receptor kinase 1; Retina-sp...      10090
    2096411  10090.ENSMUSP00000025791  ADRBK1  Adrenergic receptor kinase, beta 1; Specifical...      10090
    2105346  10090.ENSMUSP00000070445  ADRBK2  Adrenergic receptor kinase, beta 2; Specifical...      10090
    2093189  10090.ENSMUSP00000001112    GRK4  G protein-coupled receptor kinase 4; Specifica...      10090
    ...
    ```


**Pathways**

- Expected RETURN format

    | Column name | Type    |
    | ----------- | ------- |
    | pathway     | Pathway |

- Output tables:

    | nodes       |
    | ----------- |
    | id          |
    | name        |
    | description |
    | species_id  |

- Example:

    Pathways associated with a protein list (for human)

    ```
    WITH ["SFPI1", "FOSB"] as protein_names
    MATCH (protein:Protein {species_id: 9606})-[:IN]->(pathway:Pathway)
    WHERE protein.name IN protein_names
    RETURN pathway
    ```

    ```
    [nodes]
               id                        name                                        description species_id
    path:hsa05034                  Alcoholism  Alcoholism, also called dependence on alcohol ...       9606
    path:hsa05031       Amphetamine addiction  Amphetamine is a psychostimulant drug that exe...       9606
    path:hsa05030           Cocaine addiction  Drug addiction is a chronic, relapsing disorde...       9606
    path:hsa04657     IL-17 signaling pathway  The interleukin 17 (IL-17) family, a subset of...       9606
    path:hsa04380  Osteoclast differentiation  The osteoclasts, multinucleared cells originat...       9606
    ```

**Drugs, compounds & diseases**

- Expected RETURN format

    | Column name | Type     |
    | ----------- | -------- |
    | drug        | Drug     |
    | compound    | Compound |
    | disease     | Disease  |

- Output tables:

    | drugs       |
    | ----------- |
    | id          |
    | name        |

    | compounds   |
    | ----------- |
    | id          |
    | name        |

    | diseases    |
    | ----------- |
    | id          |
    | name        |

- Example:

    Diseases associated with a protein list

    ```
    WITH ["SFPI1", "FOSB"] as protein_names
    MATCH (protein:Protein)-[:IN]->(:Pathway)<-[:IN]-(disease:Disease)
    WHERE protein.name IN protein_names
    RETURN disease
    ```

    ```
    [diseases]
        id                           name
    H01611             Alcohol dependence
    H02042  Familial expansile osteolysis
    H01593                   Osteoporosis
    H00436                  Osteopetrosis
    H00437          Paget disease of bone
    ```

# More advanced Cypher queries

- Centrality for a protein list (with a score threshold of 0.7)

    Each `ASSOCIATION` relationship (edge) contains scores for different channels. `combined` score is always present and we use it to filter out insignificant interactions.

    ```
    WITH ["SFPI1", "FOSB", "MLXIPL"] as protein_names,
         9606 as species_id,
         700 as threshold
    MATCH (p1:Protein {species_id: species_id})-[a:ASSOCIATION]-(p2:Protein)
    WHERE p1.name IN protein_names AND
          p2.name IN protein_names AND
          p1.id <> p2.id AND
          a.combined >= threshold
    RETURN p1.name AS name, SUM(SIZE((p1)-[a]-(p2))) AS degree
    ORDER BY degree DESC
    ```

- Class hierarchy for a given pathway

    In this query, `chain` variable binds the whole pathway-class path in the graph.

    `*` in `-[:IN*]->` specifies a variable number of `IN` relationships between protein and class nodes. `RELATIONSHIPS()` function is used to collect those edges.

    ```
    WITH "Chemokine signaling pathway" AS pathway_name,
          9606 AS species_id
    MATCH chain = (pathway:Pathway {
            name: pathway_name,
            species_id: species_id
        }
    )-[:IN*]->(class:Class)
    RETURN pathway, class, RELATIONSHIPS(chain)
    ```
