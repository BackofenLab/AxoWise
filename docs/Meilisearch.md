# Meilisearch documentation

This README file covers the most important steps on how to set up and maintain meilisearch for the pgdb project.  
You can find the full documentation [here](https://www.meilisearch.com/docs).

## Installation - when not using our Makefile:

**only necessary when you are not using the Requirements and Makefile**

When installing meilisearch for the first time you need to download it first, use the following command:
```curl -L https://install.meilisearch.com | sh```

You can add a standard config using this command if you dont have our config file:
```curl https://raw.githubusercontent.com/meilisearch/meilisearch/latest/config.toml > config.toml ```

To test-run meilisearch use this command:
```./meilisearch --master-key="aSampleMasterKey```
Check if the config file was recognized, when starting up ypu should see **Config file path: "./config.toml"** on the terminal.

Keep the terminal open for the entire session, you should now be able to access the meilisearch preview on [_localhost:7700_](http://localhost:7700), if you are not working on a server. 


To access meilisearch through code / terminal make sure to install the meilisearch library on the **pgdb enviroment**:
```
conda activate pgdb
pip3 install meilisearch
```

Congrats! You can now use meilisearch.


## <u>First time setup:</u>

Before you start uploading data to meilisearch its important to cover a few steps. This is necessary because meilisearch will create the documents in an index in a specific way - related to its settings. If you change the settings after uploading data, all the document-indexing might need to be done again - this takes very long if it works at all.

Its best to follow these steps in the displayed order:
1. Set API Keys
2. Update the settings of the index
3. Upload the synonyms to meilisearch
4. Transform pubmed data from csv to json
5. Upload pubmed data to meilisearch


### Set API Keys:
Meilisearch uses API keys and one Master Key to manage access.

1. Adjust the **Master Key**:
   
The Master Key is set in the config file and should be secure. Use [keygen](https://randomkeygen.com/) to generate a strong Master Key and set it in the config. Restart the meilisearch client with: ```make meili_stop     make meili``` from the Makefile, the Master Key is now taken from the config file.


2. Create a file **Api_key.py**:
   
In this file create a variable: ```MASTER_KEY = "your master key"```
Now call ```python meilisearch_key.py```, you will get an output of the keys currently available on your meilisearch instance. Copy the **ADMIN KEY** and the default **SEARCH KEY** and create two more variables in the file:
```
ADMIN_API_KEY = "the admin API Key"
SEARCH_KEY = "the search key"
```

### Update index settings:
Call ```python update_config.py```:
1. *Index name:* Decide what you want to name your index
2. *Limit:* The limit defines how many results can be returned maximum, 20.000 is a sufficent limit.

The function also adjusts settings such as disabeling spelling mistakes, setting searchable and sortable attributes. 


### Upload the synonyms to meilisearch:
Call ```python meilisearch_synonyms.py```:
1. *Input file:* Give the input file with all synonyms, if you use our data it should be **genes.csv**
2. *Index:* Put the index you created earlier here

The function will process all the synonyms and sort out any that appear more than once. Once the processing has been done you can decide if you want to upload them right away -- say yes and put your index.

### Transform PubMed data from csv to json:
Before you transform your PubMed data to json make sure the attributes in the *csv_to_json.py* function match the ones from your file and their order. 
**Example** PubmedID, Title, Abstract, Cited_by, Year
If they dont match the order in ```csv-to-json()``` - adjust the code accordingly

1. Call ```python csv_to_json.py```
2. Give the input file, if you use our data - **human.csv** or **mouse.csv**
3. Set the number of abstracts that you want to have in one output file, depending on your RAM up to several million is fine, I recommend ~ 3.000.000

*This process might take a while*

The function now processes each paper and returns one or multiple json files, depending on how big your input file is. Papers with missing title or abstract are being ignored.


### Upload Pubmed data to meilisearch:
1. Adjust in the *config.toml*:
   - *http_payload_size_limit* = larger than your biggest .json file **(Watch your RAM)**
   - *max_indexing_memory* = as much as you can dedicate to meilisearch
   - *max_indexing_threads* = as many as you can dedicate to meilisearch
1. Call ```python meilisearch_add_data.py``` or ```nohup python meilisearch_add_data.py > logs.txt 2>&1 &``` to run it in the background if you didnt use the Makefile. 
2. Make sure to also run the meilisearch client in background if you want to close your ssh connection. ```nohup ./meilisearch > server_log.txt 2>&1 &```

Give the number of json files created in the *Transform Pubmed data from csv to json* function.

- If you only have one file, give the whole filename.
- If you have multiple files, just give the beginning of the filename.
  - For *Pubmed0.json, Pubmed1,json*,... only give *Pubmed*

The function will now upload one file after another to meilisearch, this may take a while, depending on how big your index already is and how many files you want to upload.

The indexing can take ~ 6h only for human data. You can check the progress with ```tail server_log.txt```. Remeber the task ID for the first upload, this way you know how many files have been uploaded successfully at a later point.


### Before the first search:
Once meilisearch is done indexing, its ready to use. Make sure that the correct index is set in ```meilisearch_query.py - get_results()``` function. 

## <u>Detailed Explanation:</u>


### Synonymy:

To create and upload synonyms you can use the **meilisearch_synonyms.py** function.

#### Using the provided function "meilisearch_synonyms.py":
This function transforms a csv file to the correct json formate and can also upload dircetly to meilisearch.

**Input file**: The input csv file should follow these requirements:
* Have four columns:
  1. Symbol - a string
  2. Alias - a list 
  3. The full name of the symbol - a string
  4. The ensembl ID - a string
   
* Symbols without aliases should either have ['no alias'] or [] set as their aliases
* Symbols without a full name should have _"not available"_ 
* The function expects this formate in the csv file:

  ```
  """POM121L2""","""['POM121-L', 'POM121L']""","""POM121-like protein 2""","""ENSMUSG00000016982"""
  """DBNL""","""['HIP-55', 'HIP55', 'SH3P7']""","""Drebrin-like protein""","""ENSMUSG00000020476"""

  ```

When executing the function you are prompted to give the input file.

You will get **two files** in return, one holding the synonym pairs, the other is the dictionary linking symbols and full_name.
In case some synonyms cant be processed they will be returned in a third file.

After processing you can **upload** the synonyms directly. Just specify the index, if it doesnt exist yet, it will be **created**.


**Please make sure to upload synonyms before you upload the data** - if done the other way around you might experience long processing times or the _too many open file discriptors_ issue.


#### Transforming the synonyms yourself:
If you want to transform the synonyms yourself make sure you provide the right formate.

In the pgdb we use multi-way synonyms, meaning they are linked both ways.
* DBNL is a synonym of HIP55
* HIP55 is a synonym of DBNL

In this example:
```
  """POM121L2""","""['POM121-L', 'POM121L']""","""POM121-like protein 2""","""ENSMUSG00000016982"""

  ```
You would need to create the following synonym pairs:
```
  'POM121L2' : ['POM121-L', 'POM121L', 'ENSMUSG00000016982']
  'POM121-L' : ['POM121L2', 'POM121L', 'ENSMUSG00000016982']
  'POM121L' : ['POM121-L', 'POM121L2', 'ENSMUSG00000016982']
  'ENSMUSG00000016982' : ['POM121-L', 'POM121L', 'POM121L2']

  ```
  as well as the full name relations:
  ```
  {
  ...
  'POM121L2' : 'POM121-like protein 2',
  'POM121-L' : 'POM121-like protein 2',
  'POM121L' :  'POM121-like protein 2',
  'ENSMUSG00000016982' : 'POM121-like protein 2',
  ...
  }
  ```


## Preparing data to be uploaded

When you want to upload data to the meilisearch database its best to provide it in json format. This section covers the conversion from _.csv_ to _.json_, but even if you have a different formate you should follow the steps.

### PubMed abstracts:

To convert from csv to json you can use the **csv_to_json.py** function.  
This function take _PubMed_ abstracts in csv formate and returns several json files.

#### Using the provided function "csv_to_json.py":

**Input file:** The input csv file has to be of a specific type, its assumed that it has 5 columns:
1. PubMed ID  - unique key
2. Title
3. Abstract
4. List of PubMed Id's that cite this one
5. Year the article was published 

If you have more or less column you can adjust the function or use your own tool.

When running the function you are asked to provide the csv filename as well as the number of rows per output file.
The number of rows relate to the rows in the csv file, its generally better to have bigger and less .json files to upload. As the whole index needs to be restructured when uploading a document

**Important:** The filesize of the output files can not be larger than the payload limit! To check you payload limit have a look at the config file under _http_payload_size_limit_. I would recommend to set the payload limit at about 6000MB and keep the .json files in the 3-4 GB range to avoid very long indexing times. **Make sure you have enough RAM or lower the limit**

#### Do your own transformation:

Please make sure that you save your data in json formate, meilisearch expects a list of dicts for each file:
```
[
    {
        PMID: 1234
        Title: "A paper"
        Abstract: "An abstract"
        Cited by: "[5786, 92882, 28282, 9999]"
        Published: 1999 
    },
    {
        ...
    }, ....

]
```
* Make sure that every elements has a **unique key**. 
  In our case thats the PMID. This attribute has to be availible in all elements!
* Create multiple output files:
  Stay below the payload limit (check config) for the filesize - I recommend files to be around 3-4GB
* Name your files correct:
  Pick a name of your choice, and name the outputfiles with ascending numbers, starting at 0:
  output0.json, output1.json, output2,json,....


  ### Api Keys:
  With *meilisearch_key.py* you can create, delete, show or save keys, just uncomment the according function call in the main function.


### Meilisearch query:
Here the user query gets preprocessed and sent to meilisearch.

- If the user query consists of a term that has a synonyms, meilisearch internally querries against these synonym terms too.

- If the user query consists of a term that has a full_name (we check for that in the *Dict_full_name.json*) we send a second query to meilisearch with the term replaced by the full name. We use "" around the full name, this way we enfore the words in the full name to appear behind each other in the results.

**Further improvment:** It might be smart to switch to multi-search in a later stage when meilisearch can process these queries in parallel. [multisearch](https://www.meilisearch.com/docs/reference/api/multi_search)






