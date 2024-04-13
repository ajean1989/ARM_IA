#!/bin/bash

set -e 

cd api
docker compose up --build -d --force-recreate
cd ..
ls
cd mlflow
docker compose up --build -d --force-recreate
cd ..
# pas de container pour automatic dataset (local)