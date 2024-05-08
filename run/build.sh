#!/bin/bash

set -e 

cd api
docker compose -f compose.yml -f compose.prod.yml up --build -d --force-recreate
cd ..
ls
cd mlflow
docker compose -f compose.yml -f compose.prod.yml up --build -d --force-recreate
cd ..
# pas de container pour automatic dataset (local)