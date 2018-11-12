
env:
	conda env create -f conda_env.yml

dump.human.psql:
	wget https://github.com/BackofenLab/cytokine-graph-db/releases/download/v0.1/dump.human.psql
	mv dump.human.psql sql/

run_tests: dump.human.psql
	bash test/run.sh
