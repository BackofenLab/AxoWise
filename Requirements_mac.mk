help:
	@echo "make prepare:		prepares the environment and installs needed libs for installation"
	@echo "make conda:          installs conda"
	@echo "make node:        	installs node"
	@echo "make java:        	installs java"
	@echo "make maven:        	installs maven (please be sure to have installed java)"
	@echo "make neo4j:        	installs neo4j (please be sure to have installed java)"
	@echo "make apoc:        	installs apoc (please be sure to have installed neo4j)"

.NOTPARALLEL:

all: prepare conda node java maven neo4j apoc

prepare:
	@echo Checking for Homebrew ...
	ifeq () # TODO: Check if Homebrew is installed
	brew update

conda:
	curl https://repo.anaconda.com/archive/Anaconda3-2023.03-1-MacOSX-x86_64.sh -o ~/Downloads/Anaconda3-2023.03-1-MacOSX-x86_64.sh
	bash ~/Downloads/Anaconda3-2023.03-1-MacOSX-x86_64.sh
	rm -r ~/Downloads/Anaconda3-2023.03-1-MacOSX-x86_64.sh
	conda --version

node:
# TODO: Needed?
# curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
	brew install node
	node --version
	npm --version

java:
	brew install openjdk@11
	java --version

maven:
	brew install maven
	mvn --version

neo4j:
# TODO: manual download
	brew install neo4j
	neo4j --version

apoc:
# dirs: https://neo4j.com/docs/operations-manual/current/configuration/file-locations/
# if error: "Unable to register procedure, because the name `apoc.export.graphml.all` is already in use." then look if too many plugins are installed!
# rm /usr/local/bin/neo4j/plugins/apoc-4.4.*
	curl https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.1/apoc-4.4.0.15-all.jar -o /usr/local/bin/neo4j/plugins/apoc-4.4.0.15-all.jar
	echo -e 'dbms.security.procedures.whitelist=apoc.export.* \napoc.import.file.use_neo4j_config=false \napoc.export.file.enabled=true' | sudo tee -a /usr/local/bin/neo4j/conf/neo4j.conf
