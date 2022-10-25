# ==================================================
# Imports
from sqlalchemy import table
from sqlalchemy import column 
from sqlalchemy import insert

import json

import subprocess as sb


# ==================================================
# Variable
with open('../secret/secret_config.json') as f:
    meta = json.load(f)
    fs = meta['first_start']
    f.close()


# ==================================================
# Main
if fs:
    print('[PENNY] Database not found. Creating instance')
    sb.run('./init_sql.sh', shell=True)
    print('[PENNY] Database initialized.')

