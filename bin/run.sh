#!/bin/sh
if [ ! -d "./penny/venv" ]; then
    cd ./penny/
    python3 -m venv venv

    source ./venv/bin/activate
    pip install --upgrade pip 
    pip install -r ../requirements.txt

    cd ..

else source ./penny/venv/bin/activate
fi 

cd ./setup/
python3 setup.py 

cd .. && cd ./penny/
python3 main.py