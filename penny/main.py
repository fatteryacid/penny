# ==================================================
# Imports
import pandas as pd

import json
import urllib.parse
import datetime

from sqlalchemy import table, column

import extract as ex
import transform as tr
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
# Variables
with open('../secret/secret_config.json') as f:
    meta = json.load(f)
    db = meta['database_information']
    config = meta['config']
    f.close()

engine_url = (f'postgresql+psycopg2://{db["db_user"]}:{urllib.parse.quote_plus(db["db_pass"])}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}')



# ==================================================
# Def main
def main():
    #Print to console
    print('[PENNY] Starting..')

    #Retrieve data
    print('[PENNY] Retrieving data...')
    data = ex.get_data(config['target_sheet'], config['worksheet_location'])
    
    #Basic data cleanup
    print('[PENNY] Cleaning data..')
    data = tr.process_colname(data)
    data = tr.process_string(data, column_list=[
        config['sheet_mapping']['id'],
        config['sheet_mapping']['item'],
        config['sheet_mapping']['category'],
        config['sheet_mapping']['subcategory'],
        config['sheet_mapping']['vendor']    
    ])
    data = tr.process_distribution(data, column_list=config['sheet_mapping']['distribution'])
    data = tr.process_amount(data)
    data = tr.process_ignore(data, config['sheet_mapping']['ignore'])

    #Formatting
    print('[PENNY] Formatting data...')
    data = tr.format_labels(data, column_list=[
        config['sheet_mapping']['category'],
        config['sheet_mapping']['subcategory'],
        config['sheet_mapping']['vendor']
    ])

    #Create db table variables
    vend = table(config['db_mapping']['vendor']['rel_name'],
            column(config['db_mapping']['vendor']['id_col']),
            column(config['db_mapping']['vendor']['desc_col'])
        )
    
    cat = table(config['db_mapping']['category']['rel_name'],
            column(config['db_mapping']['category']['id_col']),
            column(config['db_mapping']['category']['desc_col'])
        )

    sbcat = table(config['db_mapping']['subcategory']['rel_name'],
            column(config['db_mapping']['subcategory']['id_col']),
            column(config['db_mapping']['subcategory']['desc_col'])
        )

    j_type = table(config['db_mapping']['type']['rel_name'],
            column(config['db_mapping']['type']['id_col']),
            column(config['db_mapping']['type']['cat']),
            column(config['db_mapping']['type']['sbcat'])
        )

    person = table(config['db_mapping']['person']['rel_name'],
            column(config['db_mapping']['person']['id_col']),
            column(config['db_mapping']['person']['fname']),
            column(config['db_mapping']['person']['lname'])
        )

    distribution = table(config['db_mapping']['distribution']['rel_name'],
            column(config['db_mapping']['distribution']['id_col']),
            column(config['db_mapping']['distribution']['entry_id']),
            column(config['db_mapping']['distribution']['person_id'])
        )

    fact = table(config['db_mapping']['entry']['rel_name'],
            column(config['db_mapping']['entry']['id_col']),
            column(config['db_mapping']['entry']['item_desc']),
            column(config['db_mapping']['entry']['type_id']),
            column(config['db_mapping']['entry']['vend_id']),
            column(config['db_mapping']['entry']['amount']),
            column(config['db_mapping']['entry']['entry_date']),
            column(config['db_mapping']['entry']['last_updated'])
        )
    
    #Prefill categories
    #TODO: Optimize for O(n) time
    #TODO: Add logic to ignore if categories have already been prefilled
    for catlabel in db['pre_fill']['category']:
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

    #Remove variables to reduce scope errors
    del sblabel 
    del j_payload
    del cid
    del sbid

    #Check and process new vendors from extract
    print('[PENNY] Checking for new vendors...')
    cur_vendor = set()
    for i in ld.select_from(engine_url, vend):
        cur_vendor.add(i[1])

    in_vendor = data['vendor'].unique()
    new_vendor = []

    for i in in_vendor:
        if i not in cur_vendor:
            new_vendor.append(
                {config['db_mapping']['vendor']['desc_col']: i}
            )

    ld.insert_into(engine_url, vend, new_vendor)

    #Load IDs from dimension tables
    vend_dict = table_to_dict(ld.select_from(engine_url, vend))
    cat_dict = table_to_dict(ld.select_from(engine_url, cat), inverse=True)
    sbcat_dict = table_to_dict(ld.select_from(engine_url, sbcat), inverse=True)

    jt_dict = dict()
    for i in ld.select_from(engine_url, j_type):
        temp_key = cat_dict[i[1]] + sbcat_dict[i[2]]
        
        jt_dict[temp_key] = i[0]

    person_dict = dict()
    for i in ld.select_from(engine_url, person):
        person_dict[i[1]] = i[0]

    #Send to database
    print('[PENNY] Communicating with database..')
    fact_list = []
    dist_list = []
    for entry in data.itertuples():
        fact_list.append({
            'eid': entry[1],
            'item_desc': entry[3],
            #TODO: Add j_type id here
            'type_id': jt_dict[entry[5]+entry[6]],
            'vendor_id': vend_dict[entry[7]],
            'amount': entry[4],
            'entry_record_date': entry[2],
            'last_updated': datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
        })
        
        #Needs logic to also add to distribution
        #This is not a robust system to use
        #Essentially relying on positional parameters
        if entry[8] == 1:
            dist_list.append({
                "eid": entry[1],
                "person_id": person_dict[config['sheet_mapping']['distribution'][0]]
            })
            
        if entry[9] == 1:
            dist_list.append({
                "eid": entry[1],
                "person_id": person_dict[config['sheet_mapping']['distribution'][1]]
            })
            
        if entry[10] == 1:
            dist_list.append({
                "eid": entry[1],
                "person_id": person_dict[config['sheet_mapping']['distribution'][2]]
            })
        
        
    ld.insert_into(engine_url, fact, fact_list)
    ld.insert_into(engine_url, distribution, dist_list)

    print('[PENNY] Job complete. Terminating.')


# ==================================================
# Execute
if __name__ == '__main__':
    main()