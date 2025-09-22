#!/usr/bin/env bash

DATASETS_DIR="datasets"

echo "Generating datasets..."
for size in 100 1000 10000; do
    python scripts/generate_data.py --num-samples $size --out-dir "$DATASETS_DIR"
done

PYTHON_VERSIONS=("3.8" "3.10" "3.12")

for VERSION in "${PYTHON_VERSIONS[@]}"; do
    echo "Running experiments on python $VERSION..."

    docker build --build-arg PYTHON_VERSION=$VERSION -t my_experiment:$VERSION .

    docker run --rm -v "$(pwd):/app" my_experiment:$VERSION
done