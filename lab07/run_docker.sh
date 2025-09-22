#!/bin/bash

task_name=$1

if [ -z "$task_name" ]; then
    task_name="doubles" # doubles, strings, count, wiki
fi

if [ "$task_name" == "wiki" ]; then
    mkdir -p data/input
    echo "Downloading Wikipedia article"
    curl -o data/input/wiki_article.txt 'https://en.wikipedia.org/wiki/dog?action=raw'
    echo "Data saved to data/input/wiki_article.txt"
fi

echo "Resetting docker compose"
docker compose down

echo "Building docker image"
docker build -t pyflink:latest .

echo "Spinning up docker compose"
docker compose up -d

echo "Executing Flink job"
docker exec -it lab-07-jobmanager-1 /opt/flink/bin/flink run -py /opt/flink/app.py --task $task_name

echo "Done"