
env:
	conda env create -f conda_env.yml

run_tests:
	bash test/run.sh
