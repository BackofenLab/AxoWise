
env:
	conda env create -f conda_env.yml

run_tests:
	source test/run.sh
