#!/bin/sh
source ./penny/venv/bin/activate

cd ./setup/
python3 setup.py 

cd .. && cd ./penny/
python3 main.py