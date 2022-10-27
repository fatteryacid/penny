# ==================================================
# Imports
from sqlalchemy import table
from sqlalchemy import column 
from sqlalchemy import insert

import json
import subprocess as sb

import load as ld

import sys 
sys.path.insert(0, '../penny/')



# ==================================================
# Variable
path = {
    'db': './config/secret_db_conf.json',
    'gs': './config/secret_gs_conf.json',
    'sv': './config/secret_save.json'
}

with open(path['db']) as f:
    db = json.load(f)

with open(path['gs']) as f:
    gs = json.load(f)

with open(path['sv']) as f:
    sv = json.load(f)


engine_url = (f'{db["creds"]["db_engine"]}://{db["creds"]["db_user"]}:{urllib.parse.quote_plus(db["creds"]["db_pass"])}@{db["creds"]["db_host"]}:{db["creds"]["db_port"]}/{db["creds"]["db_name"]}')


# ==================================================
# Main
if sv['first_start']:
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

    #Prefill categories
    #TODO: Optimize for O(n) time if possible
    for catlabel in db['pre_fill']['category'].keys():
        sblabel = db['pre_fill']['category'][catlabel]
            
        #Build insert for d_category
        ld.insert_into(engine_url, cat, {'category_desc': catlabel})
            
        for i in sblabel:
            #Build insert for d_subcategory
            ld.insert_into(engine_url, sbcat, {'subcategory_desc': i})
                
                
            #Build insert for j_type
            cid = table_to_dict(ld.select_from(engine_url, cat))
            sbid = table_to_dict(ld.select_from(engine_url, sbcat))
                
            j_payload = {'category_id': cid[catlabel], 'subcategory_id': sbid[i]}
            ld.insert_into(engine_url, j_type, j_payload)

    #Prefill d_person
    for fname in db['pre_fill']['person'].keys():
        ld.insert_into(engine_url, person, {'first_name': fname,
                                            'last_name': db['pre_fill']['person'][fname]})