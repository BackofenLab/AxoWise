#!/bin/bash

psql -U postgres -c "DROP DATABASE string;"
psql -U postgres -c "CREATE DATABASE string;"
psql -U postgres string < dump.schema.psql
psql -U postgres string < dump.human.psql
