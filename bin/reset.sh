#!/bin/sh
dropdb penny
createdb penny

cd ../app/
cp ./secret_cache.json ./.cache.json

source ./venv/bin/activate && python3 extract.py