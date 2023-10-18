# Documentation of the Graph Database Construction Codebase

**Directories:** [/](#home), [query/](#query), [read/](#read), [upload/](#upload)

## Home (/)
**Files:** [main.py](#mainpy), [reader.py](#readerpy), [utils.py](#utilspy), [uploader.py](#uploaderpy), [querier.py](#querierpy)

### main.py
**Important Functions:** [upload_workflow()](#upload_workflow)

#### upload_workflow()
The Workflow is as follows:
1. The files are read using [read_experiment_files()](#read_experiment_files), [read_string_files()](#read_string_files), [read_ensembl_files()](#read_ensembl_files), [read_functional_files()](#read_functional_files), [read_catlas_files()](#read_catlas_files) and bring them into the appropriate format.
2. The data is uploaded using [```base_setup()```](#base_setup), [```bulk_extention()```](#bulk_extention) und [```catlas_extention()```](#catlas_extention).

#### read_experiment_files()
Reads, reformats and returns data from the bulk sequencing experiment. Uses [reading()](#reading) with mode 0.

##### Input
- genes_annotated_mouse (pandas Dataframe): Annotated Genes of form (ENSEMBL, ENTREZID, SYMBOL, annotation)

##### Return
- tg_mean_count (pandas DataFrame): Target Gene Meancount values of form (mean_count, ENSEMBL)
- tf_mean_count (pandas DataFrame): Transcription Factor Meancount values of form (mean_count, ENSEMBL)
- de_values (pandas DataFrame): Differential Expression Values from Experiment of form (ENSEMBL, Context, Value, p)
- or_nodes (pandas DataFrame): Open region nodes of form (id, annotation, feature)
- or_mean_count (pandas DataFrame): Open Region Meancount values of form (id, mean_count)
- da_values (pandas DataFrame): Differential Accesibility Values from Experiment of form (id, Context, Value, p, summit)
- tf_tg_corr (pandas DataFrame): Correlation between TG and TF of form (ENSEMBL_TG, ENSEMBL_TF, Correlation, p)
- or_tg_corr (pandas DataFrame): Correlation between TG and OR of form (ENSEMBL, Correlation, p, id)
- motif (pandas DataFrame): Motif information of form (id, or_id,ENSEMBL, Consensus, p, number_of_peaks, Concentration)
- distance (pandas DataFrame): Distance Information for Open Regions of form (id, Distance, ENSEMBL)

#### read_string_files()
Reads, reformats and returns data from STRING. Uses [reading()](#reading) with mode 1. Protein IDs must be have species prefix ("9606." for human, "10090." for mouse)

##### Input
- **complete_mouse** (pandas Dataframe): Set of Genes for Mouse from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
- **proteins_mouse** (pandas Dataframe): Set of Proteins for Mouse from ENSEMBL of form (Protein)
- **complete_human** (pandas Dataframe): Set of Genes for Humans from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
- **proteins_human** (pandas Dataframe): Set of Proteins for Humans from ENSEMBL of form (Protein)

##### Return
- genes_annotated_mouse (pandas Dataframe): Target Gene nodes for Mouse of form (ENSEMBL, ENTREZID, SYMBOL, annotation)
- proteins_annotated_mouse (pandas Dataframe): Protein nodes for Mouse of form (ENSEMBL, SYMBOL, protein_size, annotation)
- protein_protein_scores_mouse (pandas Dataframe): Scores between Proteins (STRING) for Mouse of form (Protein1, Protein2, Score)
- genes_annotated_human (pandas Dataframe): Target Gene nodes for Human of form (ENSEMBL, ENTREZID, SYMBOL, annotation)
- proteins_annotated_human (pandas Dataframe): Protein nodes for Human of form (ENSEMBL, SYMBOL, protein_size, annotation)
- protein_protein_scores_human (pandas Dataframe): Scores between Proteins (STRING) for Human of form (Protein1, Protein2, Score)

#### read_ensembl_files()
Reads, reformats and returns data from ENSEMBL. Uses [reading()](#reading) with mode 2. 

##### Return
- complete_mouse (pandas Dataframe): Set of Genes for Mouse from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
- tf_mouse (pandas Dataframe): List of Transcription factors for Mouse of form (ENSEMBL)
- proteins_mouse (pandas Dataframe): Set of Proteins for Mouse from ENSEMBL of form (Protein)
- gene_protein_link_mouse (pandas Dataframe): Links between genes and proteins for Mouse of form (ENSEMBL, Protein)
- complete_human (pandas Dataframe): Set of Genes for Human from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
- tf_human (pandas Dataframe): List of Transcription factors for Human of form (ENSEMBL)
- proteins_human (pandas Dataframe): Set of Proteins for Human from ENSEMBL of form (Protein)
- gene_protein_link_human (pandas Dataframe): Links between genes and proteins for Human of form (ENSEMBL, Protein)

#### read_functional_files()
Reads, reformats and returns data from Functional Term files. Uses [reading()](#reading) with mode 3. 

##### Return
- ft_nodes_mouse (pandas DataFrame): Functional Term nodes for Mouse of form (Term, Name, Category, Proteins)
- ft_gene_mouse (pandas DataFrame): Links between Functional Terms and Target Genes for Mouse of form (ENSEMBL, Term)
- ft_protein_mouse (pandas DataFrame): Links between Functional Terms and Proteins for Mouse of form (ENSEMBL, Term)
- ft_ft_overlap_mouse (pandas DataFrame): Overlap between Functional Terms for Mouse of form (source, target, Score)
- ft_nodes_human (pandas DataFrame): Functional Term nodes for Human of form (Term, Name, Category, Proteins)
- ft_gene_human (pandas DataFrame): Links between Functional Terms and Target Genes for Human of form (ENSEMBL, Term)
- ft_protein_human (pandas DataFrame): Links between Functional Terms and Proteins for Human of form (ENSEMBL, Term)
- ft_ft_overlap_human (pandas DataFrame): Overlap between Functional Terms for Human of form (source, target, Score)

#### read_catlas_files()
Reads, reformats and returns data from [Catlas](http://catlas.org/wholemousebrain/#!/home) Whole Mouse Brain dataset. Uses [reading()](#reading) with mode 4. 

##### Input
- or_nodes (pandas DataFrame): Existing Open region nodes of form (id, annotation, feature)
- distance (pandas DataFrame): Existing Distance edges of form (id, Distance, ENSEMBL)

##### Return
- or_extended (pandas DataFrame): Extended Open region nodes of form (id, annotation, feature)
- catlas_or_context (pandas DataFrame): Open Region Context Information in form (Context, id, cell_id)
- catlas_correlation (pandas DataFrame): OR-TG Correlation of form (id, ENSEMBL, Correlation, cell_id)
- catlas_celltype (pandas DataFrame): Celltype and Subtype info of form (name, region, nuclei_counts, celltype, subtype, sub-subtype)
- distance_extended (pandas DataFrame): Extended Distance edges of form (id, Distance, ENSEMBL)
- catlas_motifs (pandas DataFrame): Motif information of form (id, or_id, ENSEMBL, Consensus, p, number_of_peaks, Concentration, cell_id)

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

##### _DEFAULT_CATLAS_PATH
- Default value: "../source/catlas"

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
Reads Files based on Mode. It brings them into the Right format if not already existend and saves them to the ```source/processed/``` directory. Otherwise, reads them from the ```source/processed/``` directory. Uses [check_for_files()](#check_for_files) and files in [read/](#read) directory.

##### Function Calls based on Modes
- mode = 0: [parse_experiment()](#parse_experiment)
- mode = 1: [parse_string()](#parse_string)
- mode = 2: [parse_ensembl()](#parse_ensembl)
- mode = 3: [parse_functional()](#parse_functional)
- mode = 4: [parse_catlas()](#parse_catlas)
 

### utils.py
**Important Functions:** [start_driver()](#start_driver), [save_df_to_csv()](#save_df_to_csv), [get_values_reformat()](#get_values_reformat), [execute_query()](#execute_query), [check_for_files()](#check_for_files)

#### start_driver()
Starts and returns Neo4j driver.

##### Return
- driver (neo4j Driver): Started Neo4j driver 

#### stop_driver()
Stops Neo4j driver

##### Input
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

#### check_for_files()
Checks if files are in the ```source/processed/``` directory.

##### Input
- mode (Integer): Same as in [reading()](#reading)

##### Return
- True if one or more files don't exist, otherwise False

##### Files based on Mode
- mode = 0:
    - tg_mean_count.csv
    - tf_mean_count.csv
    - de_values.csv
    - or_nodes.csv
    - or_mean_count.csv
    - da_values.csv
    - tf_tg_corr.csv
    - or_tg_corr.csv
    - motif.csv
    - distance.csv
- mode = 1:
    - gene_gene_scores_mouse.csv
    - genes_annotated_mouse.csv
    - protein_protein_scores_mouse.csv
    - proteins_annotated_mouse.csv
    - gene_gene_scores_human.csv
    - genes_annotated_human.csv
    - protein_protein_scores_human.csv
    - proteins_annotated_human.csv
- mode = 2:
    - complete_mouse.csv
    - tf_mouse.csv
    - proteins_mouse.csv
    - gene_protein_link_mouse.csv
    - complete_human.csv
    - tf_human.csv
    - proteins_human.csv
    - gene_protein_link_human.csv
- mode = 3:
    - ft_nodes_mouse.csv
    - ft_gene_mouse.csv
    - ft_ft_overlap_mouse.csv
    - ft_nodes_human.csv
    - ft_gene_human.csv
    - ft_ft_overlap_human.csv
- mode = 4:
    - or_extended.csv
    - catlas_or_context.csv
    - catlas_correlation.csv
    - catlas_celltype.csv
    - distance_extended.csv
    - catlas_motifs.csv
        
        

### uploader.py
**Important Functions:** [base_setup()](#base_setup), [catlas_extention()](#catlas_extention), [bulk_extention()](#bulk_extention)

#### base_setup()
This Function Sets up the base network (Protein, Gene nodes, TF labels, Protein-Gene Links, STRING associations, Functional Terms, Overlap, TG-FT und Protein-FT links, Distance between OR and TG). Uses [start_driver()](#start_driver), [stop_driver()](#stop_driver), [setup_base_db()](#setup_base_db)

##### Input
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
Extends Database with Data from bulk sequencing experiment. Uses [start_driver()](#start_driver), [stop_driver()](#stop_driver), [extend_db_from_experiment()](#extend_db_from_experiment)

##### Input
- species (String): Representing Species (i.e. "Mus_Musculus", "Homo_Sapiens")
- tg_mean_count (pandas DataFrame): Target Gene Meancount values of form (mean_count, ENSEMBL)
- tf_mean_count (pandas DataFrame): Transcription Factor Meancount values of form (mean_count, ENSEMBL)
- or_mean_count (pandas DataFrame): Open Region Meancount values of form (id, mean_count)
- tf_tg_corr (pandas DataFrame): Correlation between TG and TF of form (ENSEMBL_TG, ENSEMBL_TF, Correlation, p)
- or_tg_corr (pandas DataFrame): Correlation between TG and OR of form (ENSEMBL, Correlation, p, id)
- motif (pandas DataFrame): Motif information of form (id, or_id,ENSEMBL, Consensus, p, number_of_peaks, Concentration) 
- tg_context_values (pandas DataFrame): Differential Expression Values from Experiment of form (ENSEMBL, Context, Value, p)
- or_context_values (pandas DataFrame): Differential Accesibility Values from Experiment of form (id, Context, Value, p, summit)

#### catlas_extention()
Extends Database with Data from [Catlas](http://catlas.org/wholemousebrain/#!/home) Whole Mouse Brain experiment. Uses [start_driver()](#start_driver), [stop_driver()](#stop_driver), [extend_db_from_catlas()](#extend_db_from_catlas)

##### Input
- species (String): Representing Species (i.e. "Mus_Musculus", "Homo_Sapiens")
- catlas_or_context (pandas DataFrame): Open Region Context Information in form (Context, id, cell_id)
- catlas_correlation (pandas DataFrame): OR-TG Correlation of form (id, ENSEMBL, Correlation, cell_id)
- catlas_celltype (pandas DataFrame): Celltype and Subtype info of form (name, region, nuclei_counts, celltype, subtype, sub-subtype)
- catlas_motifs (pandas DataFrame): Motif information of form (id, or_id, ENSEMBL, Consensus, p, number_of_peaks, Concentration, cell_id)

### querier.py
**Important Functions:** [run_queries()](#run_queries)

#### run_queries()
Runs queries from [query/query_functions.py](#queryquery_functionspy). Uses [start_driver()](#start_driver), [stop_driver()](#stop_driver).

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

#### parse_catlas()
Parses Catlas files and reformats them to fit the structure needed for uploading.

##### Source directory
Can be set with [_DEFAULT_CATLAS_PATH](#_default_catlas_path)

##### Needed Files:
- ccre/: cCRE files from [Catlas](http://catlas.org/catlas_downloads/wholemousebrain/cCREs/)
- motifs/: Motif files for each Cell- and Subtype <Catlas Cell name>_motifs.csv of forms (id, Motif, Motif ID, Log p, Concentration, ENSEMBL)
- ccre_id_dict.csv
- cell_infos.csv
- cell_specific_correlation.csv
- gene_ccre_distance.csv

##### Input
- or_nodes (pandas DataFrame): Existing Open region nodes of form (id, annotation, feature)
- distance (pandas DataFrame): Existing Distance edges of form (id, Distance, ENSEMBL)

##### Return
- or_extended (pandas DataFrame): Extended Open region nodes of form (id, annotation, feature)
- catlas_or_context (pandas DataFrame): Open Region Context Information in form (Context, id, cell_id)
- catlas_correlation (pandas DataFrame): OR-TG Correlation of form (id, ENSEMBL, Correlation, cell_id)
- catlas_celltype (pandas DataFrame): Celltype and Subtype info of form (name, region, nuclei_counts, celltype, subtype, sub-subtype)
- distance_extended (pandas DataFrame): Extended Distance edges of form (id, Distance, ENSEMBL)
- catlas_motifs (pandas DataFrame): Motif information of form (id, or_id, ENSEMBL, Consensus, p, number_of_peaks, Concentration, cell_id)

### read/read_ensembl.py

#### parse_ensembl()
Parses ENSEMBL files and reformats them to fit the structure needed for uploading.

##### Source directory
Can be set with [_DEFAULT_ENSEMBL_PATH](#_default_ensembl_path)

##### Needed Files:
- Mus_musculus.GRCm39.109.entrez.tsv
- Mus_musculus.GRCm39.109.ena.tsv
- Mus_musculus.GRCm39.109.refseq.tsv
- Mus_musculus.GRCm39.109.uniprot.tsv
- TFCheckpoint_download_180515.tsv
- lost_correlations_symbols
- Homo_sapiens.GRCh38.110.entrez.tsv
- Homo_sapiens.GRCh38.110.ena.tsv
- Homo_sapiens.GRCh38.110.refseq.tsv
- Homo_sapiens.GRCh38.110.uniprot.tsv

##### Return
- complete_mouse (pandas Dataframe): Set of Genes for Mouse from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
- tf_mouse (pandas Dataframe): List of Transcription factors for Mouse of form (ENSEMBL)
- proteins_mouse (pandas Dataframe): Set of Proteins for Mouse from ENSEMBL of form (Protein)
- gene_protein_link_mouse (pandas Dataframe): Links between genes and proteins for Mouse of form (ENSEMBL, Protein)
- complete_human (pandas Dataframe): Set of Genes for Human from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
- tf_human (pandas Dataframe): List of Transcription factors for Human of form (ENSEMBL)
- proteins_human (pandas Dataframe): Set of Proteins for Human from ENSEMBL of form (Protein)
- gene_protein_link_human (pandas Dataframe): Links between genes and proteins for Human of form (ENSEMBL, Protein)

### read/read_experiment.py

#### parse_experiment()
Parses bulk sequencing experiment files and reformats them to fit the structure needed for uploading.

##### Source directory
Can be set with [_DEFAULT_EXPERIMENT_PATH](#_default_experiment_path)

##### Needed Files:
- exp_DA.tsv
- exp_DE_filter.tsv
- correlation_pval_TF_target.csv
- corr_peak_target.csv
- TF_motif_peak.tsv
- motif_peaks_TF_no_peaks.tsv

##### Input
- genes_annotated_mouse (pandas Dataframe): Annotated Genes of form (ENSEMBL, ENTREZID, SYMBOL, annotation)

##### Return
- tg_mean_count (pandas DataFrame): Target Gene Meancount values of form (mean_count, ENSEMBL)
- tf_mean_count (pandas DataFrame): Transcription Factor Meancount values of form (mean_count, ENSEMBL)
- de_values (pandas DataFrame): Differential Expression Values from Experiment of form (ENSEMBL, Context, Value, p)
- or_nodes (pandas DataFrame): Open region nodes of form (id, annotation, feature)
- or_mean_count (pandas DataFrame): Open Region Meancount values of form (id, mean_count)
- da_values (pandas DataFrame): Differential Accesibility Values from Experiment of form (id, Context, Value, p, summit)
- tf_tg_corr (pandas DataFrame): Correlation between TG and TF of form (ENSEMBL_TG, ENSEMBL_TF, Correlation, p)
- or_tg_corr (pandas DataFrame): Correlation between TG and OR of form (ENSEMBL, Correlation, p, id)
- motif (pandas DataFrame): Motif information of form (id, or_id,ENSEMBL, Consensus, p, number_of_peaks, Concentration)
- distance (pandas DataFrame): Distance Information for Open Regions of form (id, Distance, ENSEMBL)

### read/read_functional.py

#### parse_functional()
Parses Functional term files and reformats them to fit the structure needed for uploading.

##### Source directory
Can be set with [_DEFAULT_FUNCTIONAL_PATH](#_default_functional_path)

##### Needed Files:
- functional_terms_overlap_mus_musculus.csv
- AllPathways_mouse.csv
- functional_terms_overlap_homo_sapiens.csv
- AllPathways_human.csv

##### Return
- ft_nodes_mouse (pandas DataFrame): Functional Term nodes for Mouse of form (Term, Name, Category, Proteins)
- ft_gene_mouse (pandas DataFrame): Links between Functional Terms and Target Genes for Mouse of form (ENSEMBL, Term)
- ft_protein_mouse (pandas DataFrame): Links between Functional Terms and Proteins for Mouse of form (ENSEMBL, Term)
- ft_ft_overlap_mouse (pandas DataFrame): Overlap between Functional Terms for Mouse of form (source, target, Score)
- ft_nodes_human (pandas DataFrame): Functional Term nodes for Human of form (Term, Name, Category, Proteins)
- ft_gene_human (pandas DataFrame): Links between Functional Terms and Target Genes for Human of form (ENSEMBL, Term)
- ft_protein_human (pandas DataFrame): Links between Functional Terms and Proteins for Human of form (ENSEMBL, Term)
- ft_ft_overlap_human (pandas DataFrame): Overlap between Functional Terms for Human of form (source, target, Score)

### read/read_string.py

#### parse_string()
Parses STRING files and reformats them to fit the structure needed for uploading.

##### Source directory
Can be set with [_DEFAULT_STRING_PATH](#_default_string_path)


##### Needed Files:
- 10090.protein.links.v12.0.txt
- 10090.protein.info.v12.0.tsv
- string_SYMBOL_ENSEMBL.tsv
- difference_mouse.csv
- 9606.protein.links.v12.0.txt
- 9606.protein.info.v12.0.tsv
- difference_human.csv

##### Input
- **complete_mouse** (pandas Dataframe): Set of Genes for Mouse from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
- **proteins_mouse** (pandas Dataframe): Set of Proteins for Mouse from ENSEMBL of form (Protein)
- **complete_human** (pandas Dataframe): Set of Genes for Humans from ENSEMBL of form (ENSEMBL, Protein, ENTREZID)
- **proteins_human** (pandas Dataframe): Set of Proteins for Humans from ENSEMBL of form (Protein)

##### Return
- genes_annotated_mouse (pandas Dataframe): Target Gene nodes for Mouse of form (ENSEMBL, ENTREZID, SYMBOL, annotation)
- proteins_annotated_mouse (pandas Dataframe): Protein nodes for Mouse of form (ENSEMBL, SYMBOL, protein_size, annotation)
- protein_protein_scores_mouse (pandas Dataframe): Scores between Proteins (STRING) for Mouse of form (Protein1, Protein2, Score)
- genes_annotated_human (pandas Dataframe): Target Gene nodes for Human of form (ENSEMBL, ENTREZID, SYMBOL, annotation)
- proteins_annotated_human (pandas Dataframe): Protein nodes for Human of form (ENSEMBL, SYMBOL, protein_size, annotation)
- protein_protein_scores_human (pandas Dataframe): Scores between Proteins (STRING) for Human of form (Protein1, Protein2, Score)

## query/
**Files:** [query_functions.py](#queryquery_functionspy)

### query/query_functions.py
A set of query functions.