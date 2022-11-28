#!/bin/sh
dropdb penny
createdb penny

for filename in ../setup/*; do
    if [[ $filename == *.sql ]]; then
        psql -d penny -f $filename
    else
        if [[ $filename == *.py ]]; then
            python3 $filename
        fi

    fi
done;


