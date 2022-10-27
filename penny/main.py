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
# Def main
def main():
    #Print to console
    print('[PENNY] Starting..')

    #Retrieve data
    print('[PENNY] Retrieving data...')
    data = ex.get_data(gs['target_sheet'], gs['worksheet_location'])
    
    #Basic data cleanup
    print('[PENNY] Cleaning data..')
    data = tr.process_colname(data)
    data = tr.process_string(data, column_list=[
        gs['sheet_mapping']['id'],
        gs['sheet_mapping']['item'],
        gs['sheet_mapping']['category'],
        gs['sheet_mapping']['subcategory'],
        gs['sheet_mapping']['vendor']    
    ])
    data = tr.process_distribution(data, column_list=gs['sheet_mapping']['distribution'])
    data = tr.process_amount(data)
    data = tr.process_ignore(data, gs['sheet_mapping']['ignore'])

    #Formatting
    print('[PENNY] Formatting data...')
    data = tr.trunc_df(data, sv['existing_id'])
    data = tr.format_labels(data, column_list=[
        gs['sheet_mapping']['category'],
        gs['sheet_mapping']['subcategory'],
        gs['sheet_mapping']['vendor']
    ])

    #Control for no new updates
    if len(data) > 0:

        #Save state
        last_eid = data.tail(1).iloc[0]['id']
        sv['existing_id'] = last_eid
        new_state = json.dumps(meta, indent=4)

        if type(new_state) != str:
            raise Exception('[PENNY] FATAL ERROR: Writing to config failed.')
        else:
            with open(path['sv'], 'w') as out:
                out.write(new_state)

        #Create db table variables
        vend = table(db['schema']['vendor']['rel_name'],
                column(db['schema']['vendor']['id_col']),
                column(db['schema']['vendor']['desc_col'])
            )
        
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

        distribution = table(db['schema']['distribution']['rel_name'],
                column(db['schema']['distribution']['id_col']),
                column(db['schema']['distribution']['entry_id']),
                column(db['schema']['distribution']['person_id'])
            )

        fact = table(db['schema']['entry']['rel_name'],
                column(db['schema']['entry']['id_col']),
                column(db['schema']['entry']['item_desc']),
                column(db['schema']['entry']['type_id']),
                column(db['schema']['entry']['vend_id']),
                column(db['schema']['entry']['amount']),
                column(db['schema']['entry']['entry_date']),
                column(db['schema']['entry']['last_updated'])
            )

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
                    {db['schema']['vendor']['desc_col']: i}
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
                    "person_id": person_dict[gs['sheet_mapping']['distribution'][0]]
                })
                
            if entry[9] == 1:
                dist_list.append({
                    "eid": entry[1],
                    "person_id": person_dict[gs['sheet_mapping']['distribution'][1]]
                })
                
            if entry[10] == 1:
                dist_list.append({
                    "eid": entry[1],
                    "person_id": person_dict[gs['sheet_mapping']['distribution'][2]]
                })
            
            
        ld.insert_into(engine_url, fact, fact_list)
        ld.insert_into(engine_url, distribution, dist_list)
    
    else:
        print('[PENNY] No new entries to insert.')

    print('[PENNY] Job complete. Terminating.')


# ==================================================
# Execute
if __name__ == '__main__':
    main()