#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "Missing command, use: bash $0 <command-to-run>"
    exit 1
fi

eval "$1 &"
echo "Process PID: $!"