help:
	@echo "make requirements: installs java/maven/node/... on your system"
	@echo "make env:          create conda environment"
	@echo "make neo4j:        run neo4j"
	@echo "make meili:  	  run meilisearch"
	@echo "make meili_stop:   stop meilisearch"
	@echo "make build:        builds this project"
	@echo "make update:       updates the conda environment"
	@echo "make start:        runs this project"

requirements:
	make -f Requirements.mk all

env:
	conda env create -f environment.yml

neo4j:
	sudo neo4j start

meili:
	cd backend/src/summarization/meilisearch_inhouse/; nohup ./meilisearch > meilisearch.log 2>&1 & echo $$! > meilisearch.pid

meili_stop:
	cd backend/src/summarization/meilisearch_inhouse/; sudo kill `cat meilisearch.pid` && rm -f meilisearch.pid

build:
	cd frontend; npm install; npm run build
	cd backend/gephi; mvn install

update:
	conda env update --file environment.yml --prune

start:
	echo "remember to activate your conda environment with 'conda activate pgdb'"
	echo "remember to start neo4j with 'make neo4j'"
	echo "remember to start meilisearch with 'make meili'"
	cd backend/src; sudo env "PATH=$$PATH" python main.py

deployment:
	sudo kill `cat backend/src/process.pid` > /home/ubuntu/logs/kill.log 2>&1 || true
	$(MAKE) meili_stop
	$(MAKE) update > /home/ubuntu/logs/update.log 2>&1
	$(MAKE) build > /home/ubuntu/logs/build.log 2>&1
	$(MAKE) meili
	cd backend/src; nohup sudo env "PATH=$$PATH" python main.py --pid > /home/ubuntu/logs/server.log 2>&1

lint:
	find . -name "*.py" | xargs black -l 120 --target-version=py311

test:
	# frontend
	cd frontend && npm audit --audit-level high
	# backend
	python -m unittest discover backend
	find . -name "*.py" | xargs black -l 120 --check --target-version=py311

