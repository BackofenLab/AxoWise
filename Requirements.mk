help:
	@echo "make prepare:		prepares the environment and installs needed libs for installation"
	@echo "make conda:          installs conda"
	@echo "make node:        	installs node"
	@echo "make java:        	installs java"
	@echo "make maven:        	installs maven (please be sure to have installed java)"
	@echo "make neo4j:        	installs neo4j (please be sure to have installed java)"
	@echo "make apoc:        	installs apoc (please be sure to have installed neo4j)"

.NOTPARALLEL:

all: prepare conda node java maven neo4j apoc dummydata

prepare:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	sudo apt update
	sudo apt-get update
	sudo apt install curl
	sudo apt update

conda:
# https://docs.anaconda.com/free/anaconda/install/linux/
	sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
	sudo apt-get update
	curl -o /tmp/Miniconda3-latest-Linux-x86_64.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
	bash /tmp/Miniconda3-latest-Linux-x86_64.sh
	rm /tmp/Miniconda3-latest-Linux-x86_64.sh
	conda --version

node:
# https://engineerworkshop.com/blog/how-to-install-a-specific-version-of-node-in-ubuntu-linux/
	curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
	sudo apt-get install nodejs
	node --version
	npm --version

java:
# https://wiki.ubuntuusers.de/Java/Installation/OpenJDK/
	sudo apt-get install openjdk-11-jre
	java --version

maven:
# https://phoenixnap.com/kb/install-maven-on-ubuntu
	sudo apt install maven
	mvn --version


neo4j:
# https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-neo4j-on-ubuntu-20-04
	sudo apt install curl
	curl -fsSL https://debian.neo4j.com/neotechnology.gpg.key |sudo gpg --dearmor -o /usr/share/keyrings/neo4j.gpg
	echo "deb [signed-by=/usr/share/keyrings/neo4j.gpg] https://debian.neo4j.com stable 4.4" | sudo tee -a /etc/apt/sources.list.d/neo4j.list
	sudo apt update
	sudo apt install neo4j
	neo4j --version

apoc:
# dirs: https://neo4j.com/docs/operations-manual/current/configuration/file-locations/
# if error: "Unable to register procedure, because the name `apoc.export.graphml.all` is already in use." then look if too many plugins are installed!
	sudo rm /var/lib/neo4j/plugins/apoc-4.4.* || true
	sudo wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.1/apoc-4.4.0.1-all.jar -P /var/lib/neo4j/plugins
	sudo echo -e 'dbms.security.procedures.whitelist=apoc.export.* \napoc.import.file.use_neo4j_config=false \napoc.export.file.enabled=true' | sudo tee -a /etc/neo4j/neo4j.conf

dummydata:
# file: https://drive.google.com/file/d/1YwFlqFRxTKDTjFOiUkB7T2Aeb5mVfpEr/view
# explanation: https://stackoverflow.com/questions/25010369/wget-curl-large-file-from-google-drive
# docs: https://pypi.org/project/gdown/
	pip install gdown
	cd $$HOME/Downloads && gdown 1YwFlqFRxTKDTjFOiUkB7T2Aeb5mVfpEr -O latest.dump
	sudo neo4j-admin load --from=$$HOME/Downloads/latest.dump --database=neo4j --force
	rm $$HOME/Downloads/latest.dump
