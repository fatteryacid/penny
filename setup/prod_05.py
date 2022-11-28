# ==================================================
import json

import pandas as pd
from sqlalchemy import create_engine

import urllib.parse




# ==================================================
with open('../app/secret_conf.json', 'r') as f:
    config = json.load(f)

headers = config['gs']['headers']

if 'vendor' not in headers:
    raise Exception('MissingHeaderError')


people = headers[headers.index('vendor') + 1:]

engine_url = f'{config["db"]["platform"]}://{config["db"]["user"]}:{urllib.parse.quote_plus(config["db"]["pass"])}@{config["db"]["host"]}:{config["db"]["port"]}/{config["db"]["name"]}'
engine = create_engine(engine_url)

payload = pd.DataFrame(data = people, columns = ['name'])

payload.to_sql(
    name = 'stg_people',
    con = engine,
    index = False,
    if_exists = 'replace'
)

print('CREATE TABLE << stg_people >>')