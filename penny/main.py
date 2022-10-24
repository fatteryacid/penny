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
        config['mapping']['id'],
        config['mapping']['item'],
        config['mapping']['category'],
        config['mapping']['subcategory'],
        config['mapping']['vendor']    
    ])
    data = tr.process_distribution(data, column_list=config['mapping']['distribution'])
    data = tr.process_amount(data)
    data = tr.process_ignore(data, config['mapping']['ignore'])

    #Formatting
    data = tr.format_labels(data, column_list=[
        config['mapping']['category'],
        config['mapping']['subcategory'],
        config['mapping']['vendor']
    ])



# ==================================================
# Execute
if __name__ == '__main__':
    main()