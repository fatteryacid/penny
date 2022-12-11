# ==================================================
# Imports
from Data import Data

import json
import urllib.parse
import pendulum



# ==================================================
# Notes
'''
Issue is that the logic i'm using for the extract script to stop is failing when script isc alled on no new data

'''



# ==================================================
# Def main
def main():
    last_run = False

    with open('./secret_conf.json') as f:
        gs_id = json.load(f)['gs']['sheet_id']

    inst = Data(sheet_id=gs_id)

    
    while not last_run:
        #Load fresh conf data
        with open('./secret_conf.json') as f:
            config = json.load(f)

        with open('./.cache.json') as f:
            cache = json.load(f)
            
        #Build range
        row_end = int(cache['row_start']) + int(config['penny']['batch_size'])
        select_range = str(config['gs']['col_start']) + str(cache['row_start']) + ':' + str(config['gs']['col_end']) + str(row_end)
            
        #Call API
        inst.fetch(desired_range=select_range, headers=config['gs']['headers'])

        #Breaks loop when extract is called on no new data
        if inst.size is None:
            break

        #Build IDs
        inst.enrich(config['penny']['timezone'])

        #Push to database
        engine_url = f'{config["db"]["platform"]}://{config["db"]["user"]}:{urllib.parse.quote_plus(config["db"]["pass"])}@{config["db"]["host"]}:{config["db"]["port"]}/{config["db"]["name"]}'
        inst.commit(
                engine_url = engine_url,
                rel_name = 'raw'
            )

        #Update the config
        cache['row_start'] = int(cache['row_start']) + int(inst.size) + 1
        now = pendulum.now(config['penny']['timezone'])

        cache['last_updated'] = now.to_datetime_string()

        with open('./.cache.json', 'w', encoding='utf-8') as w:
            json.dump(cache, w, ensure_ascii=False, indent=4)


        #Compare DataFrame size to expected size
        if inst.size < row_end - cache['row_start']:
            last_run = True


# ==================================================
# Execute
if __name__ == '__main__':
    main()

