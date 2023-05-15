0. Install Homebrew
1. Install java version 11 with brew
```console
brew install openjdk@11
```
2. Install neo4j manually
```console
curl https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/4.4.0.13 
```
3. Check for multiple java versions
```console
/usr/libexec/java_home -V
```
4. (Change java version to 11)
```console
export JAVA_HOME=`/usr/libexec/java_home -v <JAVA-VERSION>`
```
TODO: Change default version to 11


5. Install APOC Plugin
```console
curl https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.1/apoc-4.4.0.1-all.jar -o <NEO4J-HOME>/plugins/apoc-4.4.0.1-all.jar
```
6. Check if neo4j runs
```console
<NEO4J-HOME>/bin/neo4j console
```