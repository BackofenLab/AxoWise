# Clone Git Repository
```bash
    git clone git@github.com:BackofenLab/protein-graph-database.git
    cd protein-graph-database/
```

# Install Neo4j on Mac
## 0. Install Homebrew
```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	brew doctor # to check if homebrew is working
```

## 1. Install java version 11 with brew
```bash
brew install openjdk@11
```

## 2. Download Neo4J 4.4.20 (LTS) - Community Edition
```
https://neo4j.com/download-center/#community
```

## 3. Extract the tar file
## 4. Save Neo4J where you want it to be
```
<NEO4J-HOME> := <Path-To-Neo4j-parent-directory>/neo4j/
```

## 5. Check for multiple java versions
```bash
/usr/libexec/java_home -V
```

## 6a. (Change java version to 11)
```bash
    export JAVA_HOME=`/usr/libexec/java_home -v <JAVA-VERSION>`
```
## 6b. (Change default java version in bash)
- Open ~/.bashrc
- add this line:
```bash
    export JAVA_HOME=$(/usr/libexec/java_home -v <JAVA-VERSION>)
```
- Save and exit
TODO: Change default version to 11

## 7. Install APOC Plugin
```bash
curl https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.1/apoc-4.4.0.1-all.jar -o <NEO4J-HOME>/plugins/apoc-4.4.0.1-all.jar
```

## 8. Check if Neo4j runs
```bash
<NEO4J-HOME>/bin/neo4j console
```

## 9. OPTIONAL: Add `<NEO4J-Home>/bin/` to "PATH" if you're using bash
- Open ~/.bashrc
- add this line:
```bash
    PATH=$PATH:<NEO4J-HOME>/bin
```
- Save and exit

## 10. Create Neo4j account
- Open `localhost:7474` in your web browser.
- Login with the following credentials:
```yaml
       Username: neo4j
       Password: neo4j
       Change the password to: pgdb.
```

# Install Conda and Set up Conda Environment
### For Intel CPUs (otherwise change the Anaconda version)
```bash
    curl https://repo.anaconda.com/archive/Anaconda3-2023.03-1-MacOSX-x86_64.sh -o ~/Downloads/Anaconda3-2023.03-1-MacOSX-x86_64.sh
    bash ~/Downloads/Anaconda3-2023.03-1-MacOSX-x86_64.sh
    rm -r ~/Downloads/Anaconda3-2023.03-1-MacOSX-x86_64.sh
    conda --version
    conda env create -f environment.yml
```

### To start Conda environment
```bash
    conda activate pgdb
```

# Install Maven
```bash
    brew install maven
	mvn --version
```

# Setup dummy dataset

## 1.  Download the test sample database to your Downloads folder.
## 2.  Load the dump file into your own database.
```bash
    <NEO4J-HOME>/bin/neo4j-admin load --from=$HOME/Downloads/newmouse2db.dump --database=neo4j --force
```


# TODO: Install Frontend requirements