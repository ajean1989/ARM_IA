cd ./api
docker compose -f compose.yml -f compose.dev.yml up --build -d --force-recreate
cd ..
cd ./mlflow
docker compose -f compose.yml -f compose.dev.yml up --build -d --force-recreate
cd ..
cd ./gradio
docker compose -f compose.yml -f compose.dev.yml up --build -d --force-recreate
cd ..
