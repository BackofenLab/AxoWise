help:
	@echo "make requirements: installs java/maven/node/... on your system"
	@echo "make env:          create conda environment"
	@echo "make neo4j:        run neo4j"
	@echo "make build:        builds this project"
	@echo "make update:       updates the conda environment"
	@echo "make start:        runs this project"

requirements:
	make -f Requirements.mk all

env:
	conda env create -f environment.yml

neo4j:
	sudo neo4j start

build:
	cd frontend && \
	if [ -d "node_modules" ]; then rm -r node_modules; fi && \
	if [ -f "package-lock.json" ]; then rm package-lock.json; fi && \
	npm install && \
	npm run build && \
	cd ../backend/gephi && \
	mvn install

update:
	conda env update --file environment.yml --prune

start:
	echo "remember to activate your conda environment with 'conda activate pgdb'"
	echo "remember to start neo4j with 'make neo4j'"
	cd backend/src; sudo env "PATH=$$PATH" python main.py

deployment:
	sudo kill `cat backend/src/process.pid` > /home/ubuntu/logs/kill.log 2>&1 || true
	$(MAKE) update > /home/ubuntu/logs/update.log 2>&1
	$(MAKE) build > /home/ubuntu/logs/build.log 2>&1
	cd backend/src; nohup sudo env "PATH=$$PATH" python main.py --pid > /home/ubuntu/logs/server.log 2>&1

restart:
	sudo kill `cat backend/src/process.pid` > /home/ubuntu/logs/kill.log 2>&1 || true
	cd backend/src; nohup sudo env "PATH=$$PATH" python main.py --pid > /home/ubuntu/logs/server.log 2>&1

.PHONY: test format check-format all frontend-audit backend-test

# Run all tests (frontend + backend + formatting check)
test: frontend-audit backend-test check-format

# Frontend security audit
frontend-audit:
	cd frontend && npm audit --audit-level high

# Backend unit tests
backend-test:
	python -m unittest discover backend

# Check Python formatting without modifying files
check-format:
	black --check -l 120 --target-version=py311 . --exclude "frontend/node_modules|venv|build|dist"

# Automatically fix Python formatting issues
format:
	find . -name "*.py" | xargs black -l 120 --target-version=py311

# Run everything (check formatting, frontend audit, backend tests)
all: test
