#!/bin/bash

echo "please run build.sh before if you made changes outside of the python-backend"

echo "run backend..."
cd backend/src || exit
python main.py
