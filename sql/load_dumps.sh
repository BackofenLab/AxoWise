#!/bin/bash

psql -c "CREATE DATABASE items;"
psql items < items_schema.v10.5.sql

psql -c "CREATE DATABASE network;"
psql network < network_schema.v10.5.sql

psql -c "CREATE DATABASE evidence;"
psql evidence < evidence_schema.v10.5.sql
