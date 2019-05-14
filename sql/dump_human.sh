#!/bin/bash

pg_dump_sample -U string -h sn02.bi.uni-freiburg.de string -f dump.human.psql -m dump_manifest.human.yml
