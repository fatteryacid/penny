# ==================================================
# Imports
from sqlalchemy import table
from sqlalchemy import column 
from sqlalchemy import insert

import urllib.parse

import json
import subprocess as sb

import sys 
sys.path.insert(0, '../penny/')

import load as ld



# ==================================================
# Functions
def table_to_dict(table, inverse=False):
    payload = {}
    for a, b in table:
        if inverse:
            payload[a] = b 
        else:
            payload[b] = a

    return payload



# ==================================================
# Variable
path = {
    'db': '../penny/config/secret_db_conf.json',
    'gs': '../penny/config/secret_gs_conf.json',
    'sv': '../penny/config/secret_save.json'
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

    #Prefill categories
    cat = table(db['schema']['category']['rel_name'],
            column(db['schema']['category']['id_col']),
            column(db['schema']['category']['desc_col'])
        )

    sbcat = table(db['schema']['subcategory']['rel_name'],
            column(db['schema']['subcategory']['id_col']),
            column(db['schema']['subcategory']['desc_col'])
        )

    j_type = table(db['schema']['type']['rel_name'],
            column(db['schema']['type']['id_col']),
            column(db['schema']['type']['cat']),
            column(db['schema']['type']['sbcat'])
        )

    person = table(db['schema']['person']['rel_name'],
        column(db['schema']['person']['id_col']),
        column(db['schema']['person']['fname']),
        column(db['schema']['person']['lname'])
    )


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

    #Update save state
    sv['first_start'] = False
    out = json.dumps(sv, indent=4)
    if type(out) != str:
        raise Exception('[PENNY] FATAL ERROR: Attempted to write incorrect file to config. Suspending.')

    else:
        with open(path['sv'], 'w') as f:
            f.write(out)