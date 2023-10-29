* If your storage fills up, after repeated transactions, you might want to look at the <NEO4J-HOME>/data/transactions/neo4j/ directory, and remove the "neostore.transaction.db." files.
* You can set dbms.tx_log.rotation.retention_policy to false in the config, if you dont want to keep any transaction files
* source directory can be downloaded from: https://drive.google.com/drive/folders/1AKkq2YGMj5DoS3OsFg2zpvX4tEPtkMRX?usp=sharing
* For Ubuntu specify correct neo4j import path in the main: os.environ["_NEO4J_IMPORT_PATH"] = "/var/lib/neo4j/import"
* Make sure apoc is correctly installed and specified in the config file, on Ubuntu: /etc/neo4j/neo4j.conf. There should be a line dbms.security.procedures.whitelist=apoc.* if not add it. If apoc isnt installed at all check: https://neo4j.com/labs/apoc/4.1/installation/
* Change Database: go to "/etc/neo4j/" then edit neo4j.conf (Must be in sudo mode) locate the line dbms.default_database=neo4j and change it to dbms.default_database=<name of new database> 

