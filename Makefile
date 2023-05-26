help:
	@echo "make requirements: installs java/maven/node/... on your system"
	@echo "make env:          create conda environment"
	@echo "make neo4j:        run neo4j"
	@echo "make build:        builds this project"
	@echo "make start:        runs this project"

requirements:
	make -f Requirements.mk all

env:
	conda env create -f environment.yml

neo4j:
	sudo neo4j start

build:
	cd frontend; npm install; npm run build
	cd backend/gephi; mvn install

start:
	echo "remember to activate your conda environent with 'conda activate pgdb'"
	echo "remember to start neo4j with 'make neo4j'"
	cd backend/src; sudo env "PATH=$$PATH" python main.py

lint:
	find . -name "*.py" | xargs black -l 120 --target-version=py311

test:
	find . -name "*.py" | xargs black -l 120 --check --target-version=py311

