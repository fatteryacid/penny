# ==================================================
# Imports
from sqlalchemy import table
from sqlalchemy import column 
from sqlalchemy import insert

import json

import subprocess as sb


# ==================================================
# Variable
with open('../penny/config.json') as f:
    meta = json.load(f)
    fs = meta['first_start']
    f.close()


# ==================================================
# Main
if fs:
    print('[PENNY] Database not found. Creating instance')
    enable = 'chmod +x ./init_sql.sh'
    process = sb.Popen(enable.split(), stdout=sb.PIPE)
    output, error = process.communicate()
    sb.run('./init_sql.sh', shell=True)
    print('[PENNY] Database initialized.')

    meta['first_start'] = False
    out = json.dumps(meta, indent=4)
    if type(out) != str:
        raise Exception('[PENNY] FATAL ERROR: Attempted to write incorrect file to config. Suspending.')

    else:
        with open('../penny/config.json', 'w') as f:
            f.write(out)

