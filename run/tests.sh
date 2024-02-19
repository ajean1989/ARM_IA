#!/bin/bash

set -e 

cd api
docker compose up --build -d --force-recreate
cd ..

cd tests_fonctionnels_api
docker compose up --build -d --force-recreate
cd ..