# ==================================================
# Imports
import pandas as pd

import json
import urllib.parse

from sqlalchemy import table, column

import extract as ex
import transform as tr
import load as ld


# ==================================================
# Functions
def table_to_dict(table, three=False):
    payload = {}
    if three:
        for a, b, c in table:
            payload[str(b) + str(c)] = a
    else:
        for a, b in table:
            payload[b] = a

    return payload



# ==================================================
# Variables
with open('../secret/secret_config.json') as f:
    meta = json.load(f)
    db = meta['database_information']
    config = meta['config']
    f.close()

engine_url = (f'postgresql+psycopg2://{db["db-user"]}:{urllib.parse.quote_plus(db["db-pass"])}@{db["db-host"]}:{db["db-port"]}/{db["db-name"]}')



# ==================================================
# Def main
def main():
    #Retrieve data
    data = ld.get_data(config['target_sheet'], config['worksheet_location'])
    
    #Basic data cleanup
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
            column(config['db_mapping']['entry']['cat_id']),
            column(config['db_mapping']['entry']['sbcat_id']),
            column(config['db_mapping']['entry']['vend_id']),
            column(config['db_mapping']['entry']['amount']),
            column(config['db_mapping']['entry']['entry_date']),
            column(config['db_mapping']['entry']['last_updated'])
        )

    #Check and process new vendors from extract
    cur_vendor = set()
    for i in ld.select_from(engine_url, vend):
        cur_vendor.add(i[1])

    in_vendor = f['vendor'].unique()
    new_vendor = []

    for i in in_vendor:
        if i not in cur_vendor:
            new_vendor.append(
                {config['db_mapping']['vendor']['desc_col']: i}
            )

    ld.insert_into(engine_url, vend, new_vendor)

    #Load IDs from dimension tables
    vend_dict = table_to_dict(ld.select_from(engine_url, vend))
    cat_dict = table_to_dict(ld.select_from(engine_url, cat))
    sbcat_dict = table_to_dict(ld.select_from(engine_url, sbcat))
    person_dict = table_to_dict(ld.select_from(engine_url, person), three=True)

    #Send to database
    send_list = []
    for entry in f.itertuples():
        send_list.append({
            'eid': entry[1],
            'item_desc': entry[3],
            'category_id': cat_dict[entry[5]],
            'subcategory_id': sbcat_dict[entry[6]],
            'vendor_id': vend_dict[entry[7]],
            'amount': entry[4],
            'entry_record_date': entry[2],
            'last_updated': datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
        })

    ld.insert_into(engine_url, fact, send_list)


# ==================================================
# Execute
if __name__ == '__main__':
    main()