#!/bin/bash

pg_dump_sample -U string -h sn02.bi.uni-freiburg.de string -f dump.mouse.psql -m dump_manifest.mouse.yml
