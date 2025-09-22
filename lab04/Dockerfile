ARG PYTHON_VERSION=3.10
FROM python:$PYTHON_VERSION

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip

RUN if [ "$PYTHON_VERSION" = "3.8" ]; then \
        pip install numpy==1.21 pandas==1.3 matplotlib==3.4; \
    elif [ "$PYTHON_VERSION" = "3.10" ]; then \
        pip install numpy==1.26.4 pandas==1.5.3 matplotlib; \
    else \
        pip install -r requirements.txt; \
    fi

CMD ["python", "scripts/run_experiments.py", "--datasets-dir", "datasets"]

