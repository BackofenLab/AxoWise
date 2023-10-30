* If your storage fills up, after repeated transactions, you might want to look at the <NEO4J-HOME>/data/transactions/neo4j/ directory, and remove the "neostore.transaction.db." files.
* You can set dbms.tx_log.rotation.retention_policy to false in the config, if you dont want to keep any transaction files
* source directory can be downloaded from: https://drive.google.com/drive/folders/1AKkq2YGMj5DoS3OsFg2zpvX4tEPtkMRX?usp=sharing
* For Ubuntu specify correct neo4j import path in the main: os.environ["_NEO4J_IMPORT_PATH"] = "/var/lib/neo4j/import"
* Make sure apoc is correctly installed and specified in the config file, on Ubuntu: /etc/neo4j/neo4j.conf. There should be a line dbms.security.procedures.whitelist=apoc.* if not add it. If apoc isnt installed at all check: https://neo4j.com/labs/apoc/4.1/installation/
* Change Database: go to "/etc/neo4j/" then edit neo4j.conf (Must be in sudo mode) locate the line dbms.default_database=neo4j and change it to dbms.default_database=<name of new database> 

## How to add a database and switch between databases on Ubuntu (Neo4j community edition)
1. Stop neo4j if it is running.
2. Edit neo4j.conf (In my case it was under /etc/neo4j
3. Find the line "dbms.active_database=" if doing this for the first time dont forget to uncomment the line!
4. Replace the value in the line to the name of the database that you wish to add.
5. Start neo4j
6. To make sure that a new database was created run "SHOW DATABASES" in neo4j of the browser, it should show all databases that are on the system. In particular the database that has just been added should show up as online.
7. Follow the same procedure to switch to an already existant database.
