#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "Missing command, use: bash $0 <command-to-kill>"
    exit 1
fi

PID=$(pidof "$1")

if [ -z "$PID" ]; then
    echo "No process found"
    exit 1
fi

kill $PID
echo "Process '$1' (PID: $PID) killed."
