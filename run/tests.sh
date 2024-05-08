#!/bin/bash

set -e 

cd api
docker compose -f compose.yml -f compose.test.yml up --build -d --force-recreate
cd ..

cd mlflow
docker compose -f compose.yml -f compose.test.yml up --build -d --force-recreate
cd ..
# pas de container pour automatic dataset (local)

cd tests_fonctionnels_api
docker compose up --build -d --force-recreate
cd ..