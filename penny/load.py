# ==================================================
# Imports
import pandas pd 
from sqlalchemy import create_engine
from sqlalchemy import text


# ==================================================
# Functions
def get_vendors(engine_url):
    #Create SQL Statement
    db = create_engine(engine_url)
    vend = table('d_vendor',
                column('vendor_id'),
                column('vendor_desc')
            )
    
    stmt = select(vend.c.vendor_id.distinct(), vend.c.vendor_desc)
    
    #Send query to DB
    with db.connect() as conn:
        result = conn.execute(stmt)
        payload = []
        
        for i in result:
            payload.append(i)
            
        conn.close()
    
    db.dispose()
    return payload


def insert_vendors(engine_url, new_vendor_list):
    db = create_engine(engine_url)
    vend = table('d_vendor',
                column('vendor_desc')
            )
    
    payload = []
    
    for i in new_vendor_list:
        payload.append({'vendor_desc': str(i)})
        
    with db.connect() as conn:
        insert = vend.insert()
        conn.execute(insert, payload)
        
        conn.close()
        
    db.dispose()
            


def load_to_db(df, engine, behavior):
    with engine.connect() as conn:
        conn.execute(
            text(f'INSERT INTO ')
        )
