#!/bin/bash

pg_dump -U string -h sn02.bi.uni-freiburg.de \
	--schema-only \
	--schema=items \
	--schema=network \
	--schema=evidence \
	--format=p \
	--no-owner \
	> dump.schema.psql
