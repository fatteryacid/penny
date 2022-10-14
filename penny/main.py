# ==================================================
# Imports
import json
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy import text

import psycopg2 as pg 


# ==================================================
# Variables
with open('../secret/secret.json') as f:
    login = json.load(f)
    f.close()

engine = create_engine(f'postgresql+psycopg2://{login["db-user"]}:{urllib.parse.quote_plus(login["db-pass"])}@{login["db-host"]}:{login["db-port"]}/{login["db-name"]}')



# ==================================================
# Def main
def main():

    with engine.connect() as connection:
        result = connection.execute(text("select username from users"))
        for row in result:
            print("username:", row["username"])



# ==================================================
# Execute
if __name__ == '__main__':
    main()