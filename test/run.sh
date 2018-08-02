#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)
python test/test_sql_queries.py
