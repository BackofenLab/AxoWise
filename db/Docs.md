# Code documentation of the Graph Database construction

Directories: [./](#home), [query/](#query), [read/](#read), [upload/](#upload)

## Home (./)
**Files:** [main.py](#mainpy), [reader.py](#readerpy), [utils.py](#utilspy), [uploader.py](#uploaderpy), [querier.py](#querierpy)

### main.py
**Important Functions:** [upload_workflow()](#upload_workflow)

#### upload_workflow()
The Workflow is as follows:
1. The files are read using [```read_xxx()```](#readerpy) and returned in the appropriate format.
2. The data is uploaded using [```base_setup()```](#base_setup), [```bulk_extention()```](#bulk_extention) und [```catlas_extention()```](#catlas_extention).

#### Enviromnemt Variables
Can be set at the beginning of [main.py](#mainpy).

##### _DEFAULT_EXPERIMENT_PATH
- Default value: "../source/experiment"

##### _DEFAULT_STRING_PATH
- Default value: "../source/string"

##### _DEFAULT_FUNCTIONAL_PATH
- Default value: "../source/functional"

##### _DEFAULT_ENSEMBL_PATH
- Default value: "../source/ensembl"

##### _DEFAULT_CREDENTIALS_PATH
- Default value: "../../config.yml"

##### _DEV_MAX_REL
- Default value: "10000"

##### _NEO4J_IMPORT_PATH
- Default value: "/usr/local/bin/neo4j/import/"

##### _FUNCTION_TIME_PATH
- Default value: "../source/timing/function_times.tsv"

##### _TIME_FUNCTIONS
- Default value: "False"

##### _SILENT
- Default value: "False"

##### _PRODUCTION
- Default value: "True"

##### _ACCESS_NEO4J
- Default value: "True"

### reader.py
**Important Functions:** [reading()](#reading)
#### reading() 

### utils.py
**Important Functions:** [start_driver()](#start_driver), [save_df_to_csv()](#save_df_to_csv), [get_values_reformat()](#get_values_reformat), [execute_query()](#execute_query)

#### start_driver()
Starts and returns neo4j driver.

##### Return
- driver (neo4j Driver): Started Neo4j driver 

#### save_df_to_csv()
Saves the Dataframe to a csv in the Neo4j import directory (as defined in [_NEO4J_IMPORT_PATH](#_neo4j_import_path))

##### Input
- file_name (String): File name of the file to be created (used later by [create_nodes()](#create_nodes) and [create_relationship()](#create_relationship))
- df (pandas DataFrame): Dataframe to be saved
- override_prod (bool): If True, overrides [_PRODUCTION](#_production), if _PRODUCTION and override_prod are False, df of length [_DEV_MAX_REL](#_dev_max_rel) is saved (Default: False)

#### get_values_reformat()

##### Input
- df (pandas DataFrame): Dataframe of Values
- match (List[String]): Unique IDs as a subset of columns

##### Return
- values (List[String]): All Values apart from Values in ```match```
- reformat (List[Tuple[String]]): Values for be formatted from String to Integer/Float using Cypher (e.g. [("Correlation", "toFloat")])

#### execute_query()
Executes given query

##### Input

- query (String): Cypher Query as a String
- read (bool): If True, query is read-only (Default: False)
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))

### uploader.py
**Important Functions:** [base_setup()](#base_setup), [catlas_extention()](#catlas_extention), [bulk_extention()](#bulk_extention)

#### base_setup()
This Function Sets up the base network (Protein, Gene nodes, TF labels, Protein-Gene Links, STRING associations, Functional Terms, Overlap, TG-FT und Protein-FT links, Distance between OR and TG)

##### Input: 
- species (String): Representing Species (i.e. "Mus_Musculus", "Homo_Sapiens")
- gene_nodes (pandas DataFrame): Target Gene nodes of form (ENSEMBL, ENTREZID, SYMBOL, annotation)
- ft_nodes (pandas DataFrame): Functional Term nodes of form (Term, Name, Category, Proteins)
- ft_ft_overlap (pandas DataFrame): Overlap between Functional Terms of form (source, target, Score)
- ft_gene (pandas DataFrame): Links between Functional Terms and Target Genes of form (ENSEMBL, Term)
- tf (pandas DataFrame): List of Transcription factors (subset of TGs, must be still included in gene_nodes) of form (ENSEMBL)
- ft_protein (pandas DataFrame): Links between Functional Terms and Proteins of form (ENSEMBL, Term)
- gene_protein_link (pandas Dataframe): Links between genes and proteins of form (ENSEMBL, Protein)
- proteins_annotated (pandas DataFrame): Protein nodes of form (ENSEMBL, SYMBOL, protein_size, annotation)
- protein_protein_scores (pandas DataFrame): Scores between Proteins (STRING) of form (Protein1, Protein2, Score)
- or_nodes (pandas DataFrame): Open chromatin region nodes of form (id, annotation, feature)
- distance (pandas DataFrame): Distance between OR and TG of form (id, Distance, ENSEMBL, Dummy)

#### bulk_extention()

##### Input:

#### catlas_extention()

##### Input:

### querier.py

## upload/
**Files:** [upload_experiment.py](#uploadupload_experimentpy), [upload_base.py](#uploadupload_basepy), [upload_functions.py](#uploadupload_functionspy), [upload_catlas.py](#uploadupload_catlaspy)

### upload/upload_experiment.py
This file has several functions to ease the upload of experiments, while they must be combined to fit the experiment used. It is also the file in which the bulk-seq experiment is uploaded.
**Important Functions:** [extend_db_from_experiment()](#extend_db_from_experiment), [create_study_cell_source_meancount()](#create_study_cell_source_meancount), [create_context()](#create_context), [create_motif()](#create_motif), [create_correlation()](#create_correlation)

#### extend_db_from_experiment()
Must be written for new experiments so that the experiment data is appropriate.
Calls other functions to upload the given data.

#### create_study_cell_source_meancount()
This function is also Data specific. 
It creates the Study, Celltype (if needed), and Source node (and for this experiment a MeanCount node)

#### create_tg_meancount()
[create_context()](#create_context) should be used

#### create_tf_meancount()
[create_context()](#create_context) should be used

#### create_or_meancount()
[create_context()](#create_context) should be used

#### create_context()
Creates Context nodes, HAS edges from Source to Context, and VALUE edges from Context to either TG or OR nodes. Uses [create_nodes()](#create_nodes), [create_relationship()](#create_relationship), [get_values_reformat()](#get_values_reformat), [save_df_to_csv()](#save_df_to_csv)

##### Input
- context (pandas DataFrame): Dataframe with Contexts, Values, and entities (TG or OR) of form (ENSEMBL, Context, **Values) for TGs, (id, Context, **Values) for ORs
- context_type (String): Context Type (e.g. "Timeframe", "MeanCount", "Location")
- source (Integer): ID of Source node
- value_type (Integer): Indicator which entity this data is linked to (0 -> Open Region, 1 -> Target Gene)
- species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))

#### create_motif()
Creates MOTIF edges between TF and OR nodes. Uses [create_relationship()](#create_relationship), [get_values_reformat()](#get_values_reformat), [save_df_to_csv()](#save_df_to_csv)

##### Input
- motif (pandas DataFrame): DataFrame with Motif information of form (or_id, ENSEMBL, Consensus, id, **Additional Values)
- source (Integer): ID of Source node
- species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))

#### create_correlation()
Creates CORRELATION edges between entities Uses [create_relationship()](#create_relationship), [get_values_reformat()](#get_values_reformat), [save_df_to_csv()](#save_df_to_csv)

##### Input
- correlation (pandas DataFrame): Dataframe with Correlation (+ additional) values and entities of form (ENSEMBL, id, Correlation, p) for OR-TG, (ENSEMBL_TG, ENSEMBL_TF, Correlation, p) for TF-TG
- source (Integer): ID of Source node
- value_type (Integer): Indicator which entitis are to be linked linked to (0 -> TG-OR, 1 -> TF-TG)
- species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))


### upload/upload_functions.py
**Important Functions:** [create_nodes()](#create_nodes), [update_nodes()](#update_nodes), [create_relationship()](#create_relationship)

#### create_nodes()
Generates and runs Query to upload nodes to the DB. Uses [execute_query()](#execute_query)

##### Input
- source_file (String): Filename where data is (same as in [save_df_to_csv()](#save_df_to_csv))
- type_ (String): Type of node (e.g. "TG", "TG:TF", etc.)
- id (String): unique identifier of node (e.g. "ENSEMBL" for TG nodes)
- values (List[String]): include all properties without node identifier (e.g. ["SYMBOL", "annotation"])
- reformat_values (List[Tuple[String]]): Values for be formatted from String to Integer/Float using Cypher functions (computed by [get_values_reformat()](#get_values_reformat)) e.g. [("Correlation", "toFloat")]
- species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))
- merge (bool): If True "MERGE" is used, else "CREATE" is used (Default: True)

#### update_nodes()
Generates and runs Query to update node properties. Should be used with caution, not propperly tested. Uses [execute_query()](#execute_query)

#### create_relationship()
Generates and runs Query to upload edges to the DB. Uses [execute_query()](#execute_query)

##### Input
- source_file (String): Filename where data is (same as in [save_df_to_csv()](#save_df_to_csv))
- type_ (String): Edge type (e.g. "CORRELATION")
- between (Tuple[Tuple[String]]): Node identifiers of nodes between which the edge is to be created Form is ((<Database ID for Node 1>, <Column name in csv for Database ID for Node 1>), (<Database ID for Node 2>, <Column name in csv for Database ID for Node 2>)) (e.g. (("ENSEMBL", "ENSEMBL_TF"), ("ENSEMBL", "ENSEMBL_TG")) from [create_correlation()](#create_correlation))
- node_types (Tuple[String]): Node types between which the edge is to be created
- values (List[String]): Values include all properties without node identifiers 
- reformat_values: (List[Tuple[String]]): Values for be formatted from String to Integer/Float using Cypher
- species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))
- merge (bool): If True "MERGE" is used, else "CREATE" is used (Default: True)
- bidirectional (bool): If True Query is of form -[]-, else -[]->. Not unidirectionality is highly recommended (Default: False)

### upload/upload_base.py
**Important Functions:** [create_gene_nodes()](#create_gene_nodes), [create_protein_nodes()](#create_protein_nodes), [create_gene_protein_edges()](#create_gene_protein_edges), [create_tf_label()](#create_tf_label), [create_or_nodes()](#create_or_nodes), [create_distance_edges()](#create_distance_edges), [create_string()](#create_string), [create_functional()](#create_functional), [setup_base_db()](#setup_base_db)

#### create_gene_nodes()
Creates Gene Nodes based on ENSEMBL Data (with annotations from STRING). Uses [create_nodes()](#create_nodes), [get_values_reformat()](#get_values_reformat), [save_df_to_csv()](#save_df_to_csv)

##### Input
- nodes (pandas Dataframe): Node info of form (ENSEMBL, ENTREZID, SYMBOL, annotation)
- species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))

#### create_protein_nodes()
Creates Protein Nodes based on ENSEMBL Data (with annotations from STRING). Uses [create_nodes()](#create_nodes), [get_values_reformat()](#get_values_reformat), [save_df_to_csv()](#save_df_to_csv)

##### Input
- nodes (pandas Dataframe): Protein info of form (ENSEMBL, SYMBOL, protein_size, annotation)
- species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))


#### create_gene_protein_edges()
Creates PRODUCT edges between TG and Protein nodes. Uses [create_relationship()](#create_relationship), [get_values_reformat()](#get_values_reformat), [save_df_to_csv()](#save_df_to_csv)

##### Input 
- links (pandas DataFrame): Links between Genes and Proteins as given from ENSEMBL of form (ENSEMBL, Protein)
- species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))

#### create_tf_label()
Sets TF label to TG nodes
Uses [update_nodes()](#update_nodes), [get_values_reformat()](#get_values_reformat), [save_df_to_csv()](#save_df_to_csv)

##### Input
- tf (pandas DataFrame): List of Transcription Factors of form (ENSEMBL)
- species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))


#### create_or_nodes()
Creates OR nodes from Dataframe. Uses [create_nodes()](#create_nodes), [get_values_reformat()](#get_values_reformat), [save_df_to_csv()](#save_df_to_csv)

##### Input
- nodes (pandas DataFrame): List of Open regions to be added of form (id, annotation, feature)
- species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))

#### create_distance_edges()
Creates DISTANCE edges between OR and TG. Uses [create_relationship()](#create_relationship), [get_values_reformat()](#get_values_reformat), [save_df_to_csv()](#save_df_to_csv)

##### Input
- distance (pandas DataFrame): Distance information of form (id, Distance, ENSEMBL, Dummy)
- species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))

#### create_string()
Creates STRING edges from STRING association scores. Uses [create_relationship()](#create_relationship), [get_values_reformat()](#get_values_reformat), [save_df_to_csv()](#save_df_to_csv)

##### Input
- protein_protein_scores (pandas DataFrame): Edge information of form (Protein1, Protein2, Score)
- species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))

#### create_functional()
Creates functional term nodes, OVERLAP edges, and LINKs to TG and Protein nodes. Uses [create_nodes()](#create_nodes), [create_relationship()](#create_relationship), [get_values_reformat()](#get_values_reformat), [save_df_to_csv()](#save_df_to_csv)

##### Input
- ft_nodes (pandas DataFrame): Functional Term nodes of form (Term, Name, Category, Proteins)
- ft_ft_overlap (pandas DataFrame): Overlap edges of form (source, target, Score)
- ft_gene (pandas DataFrame): FT-Gene edges of form (ENSEMBL, Term)
- ft_protein (pandas DataFrame): FT-Protein edges of form (ENSEMBL, Term)
- species (String): Species Identifier (i.e. "Mus_Musculus", "Homo_Sapiens")
- driver (neo4j Driver): Started Neo4j driver (can be done with [start_driver()](#start_driver))

#### setup_base_db()
Sets up the database without experiments. Uses [create_gene_nodes()](#create_gene_nodes), [create_protein_nodes()](#create_protein_nodes), [create_gene_protein_edges()](#create_gene_protein_edges), [create_tf_label()](#create_tf_label), [create_or_nodes()](#create_or_nodes), [create_distance_edges()](#create_distance_edges), [create_string()](#create_string), [create_functional()](#create_functional)

### upload/upload_catlas.py
**Important Functions:** [create_source()](#create_source), [extend_db_from_catlas()](#extend_db_from_catlas)

#### create_source()
Experiment specific function to Create Celltype, Subtype, Study, and Source nodes. Cannot be reused.

#### extend_db_from_catlas()
Extends the Database with the [Catlas](http://catlas.org/wholemousebrain/#!/home) Whole Mouse Brain experiment data. This function is specific to the experiment.
Uses [create_source()](#create_source), [create_context()](#create_context), [create_correlation()](#create_correlation), [create_motif()](#create_motif)

## read/
Everything in this directory is specific to the input datafiles (and -names).
**Files:** [read_catlas.py](#readread_catlaspy), [read_ensembl.py](#readread_ensemblpy), [read_experiment.py](#readread_experimentpy), [read_functional.py](#readread_functionalpy), [read_string.py](#readread_stringpy)

### read/read_catlas.py

### read/read_ensembl.py

### read/read_experiment.py

### read/read_functional.py

### read/read_string.py

## query/
**Files:** [query_functions.py](#queryquery_functionspy)

### query/query_functions.py