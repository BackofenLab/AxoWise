#!/bin/bash

TEST_DIR=$(pwd)
cd ..
export PYTHONPATH=$PYTHONPATH:$(pwd)
python test/test_sql_queries.py
cd $TEST_DIR
