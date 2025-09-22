FROM apache/flink:latest

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip3 install apache-flink

RUN mkdir -p /opt/flink/data

COPY app.py /opt/flink/app.py

WORKDIR /opt/flink