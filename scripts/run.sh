#!/bin/bash

echo "building frontend..."
cd frontend || exit
npm install
npm run build
cd ..

echo "building backend..."
cd backend/gephi || exit
mvn install
cd ../..

echo "run backend..."
cd backend/src || exit
python main.py