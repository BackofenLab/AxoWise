help:
	@echo "make requirements: installs java/maven/node/... on your system"
	@echo "make env:          create conda environment"
	@echo "make neo4j:        run neo4j"
	@echo "make build:        builds this project"
	@echo "make start:        runs this project"

requirements:

	cd docs/installation; make all

env:
	conda env create -f environment.yml

neo4j:
	sudo neo4j start

build:
	cd frontend/sigma.js-1.2.0; npm install; npm run build;
	cd frontend; npm install; npm run build
	cd backend/gephi; mvn install

start:
	echo "remember to start neo4j with 'make neo4j'"
	cd backend/src; python main.py

test:
	# check syntax
	find . -name "*.py" | xargs pylint -E
