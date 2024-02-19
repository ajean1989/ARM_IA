#!/bin/bash

set -e 

cd api
docker compose up --build -d --force-recreate
cd ..