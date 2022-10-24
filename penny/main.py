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
            column(['db_mapping']['vendor']['id_col']),
            column(['db_mapping']['vendor']['desc_col'])
        )
    
    cat = table(config['db_mapping']['category']['rel_name'],
            column(['db_mapping']['category']['id_col']),
            column(['db_mapping']['category']['desc_col'])
        )

    sbcat = table(config['db_mapping']['subcategory']['rel_name'],
            column(['db_mapping']['subcategory']['id_col']),
            column(['db_mapping']['subcategory']['desc_col'])
        )



# ==================================================
# Execute
if __name__ == '__main__':
    main()