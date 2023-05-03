all: prefix conda node java maven neo4j

prefix:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	sudo apt update
	sudo apt-get update
	sudo apt install curl
	sudo apt update

conda:
# https://docs.anaconda.com/free/anaconda/install/linux/
	sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
	sudo apt-get update
	cd ~/Downloads; sudo wget https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh
	bash ~/Downloads/Anaconda3-2023.03-1-Linux-x86_64.sh
	rm -rf ~/Downloads/Anaconda3-2023.03-1-Linux-x86_64.sh
	conda --version

node:
# https://engineerworkshop.com/blog/how-to-install-a-specific-version-of-node-in-ubuntu-linux/
	curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
	sudo apt-get install nodejs npm
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
	sudo wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.4.0.1/apoc-4.4.0.1-all.jar -P /var/lib/neo4j/plugins
	sudo echo -e 'dbms.security.procedures.whitelist=apoc.export.* \napoc.import.file.use_neo4j_config=false \napoc.export.file.enabled=true' | sudo tee -a /etc/neo4j/neo4j.conf
