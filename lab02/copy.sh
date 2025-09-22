#!/usr/bin/env bash

if [ "$#" -lt 3 ]; then
    echo "Missing command, use: bash $0 <user1@source:/path/> <user2@destination:/path/> <file1>:<newname> ...]"
    exit 1
fi

source_server=$1
destination_server=$2
shift 2

for file in "$@"; do
    if [[ "$file" == *:* ]]; then
        original_name=$(echo "$file" | cut -d':' -f1)
        new_name=$(echo "$file" | cut -d':' -f2)
        scp "${source_server}/${original_name}" "${destination_server}/${new_name}"
    else
        original_name=$file
        scp "${source_server}/${original_name}" "${destination_server}/${original_name}"
    fi

    if [ $? -ne 0 ]; then
        echo "Copying file $original_name failed"
    else
        echo "Copying file $original_name completed"
    fi
done