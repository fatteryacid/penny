# ==================================================
# Imports
import pandas pd 
from sqlalchemy import create_engine
from sqlalchemy import text


# ==================================================
# Functions
def check_vendors(df, engine):
    df['store'].drop_duplicates(inplace=True)
    

    with engine.connect() as conn:
        db_list = conn.execute(
            text('SELECT DISTINCT vendor_desc FROM d_vendors')
        )

            


def load_to_db(df, engine, behavior):
    with engine.connect() as conn:
        conn.execute(
            text(f'INSERT INTO ')
        )
