# ==================================================
# Imports
import pandas pd 
from sqlalchemy import create_engine
from sqlalchemy import table 
from sqlalchemy import column
from sqlalchemy import select
from sqlalchemy import distinct
from sqlalchemy import exc 


# ==================================================
# Functions
def get_vendors(engine_url):
    db = create_engine(engine_url)
    vend = table('d_vendor',
                column('vendor_id'),
                column('vendor_desc')
            )
    
    stmt = select(vend.c.vendor_id.distinct(), vend.c.vendor_desc)
    
    #Make connection
    with db.connect() as conn:
        result = conn.execute(stmt)
        payload = {}
        
        for i in result:
            payload[i[1]] = i[0]
            
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
        
    try:
        with db.connect() as conn:
            insert = vend.insert()
            conn.execute(insert, payload)
            conn.close()
    except exc.IntegrityError:
        print('WARNING: Attempted to create duplicate data.')
    
    db.dispose()


def select_from(engine_url, table_object):
    db = create_engine(engine_url)
    stmt = select(table_object)
    
    #Make connection
    with db.connect() as conn:
        result = conn.execute(stmt).fetchall()
        conn.close()
    
    db.dispose()
    
    #Catch empty return or more than 1 return
    if len(result) <= 0:
        raise Exception('FATAL: Search returned empty ID.')
    
    else:
        return result

def insert_into(engine_url, table_object, value_list):
    if len(value_list) <= 0:
        print('WARNING: No values to insert.')
        return
    
    db = create_engine(engine_url)
    
    with db.connect() as conn:
        result = conn.execute(
            insert(table_object),
            value_list
        )
        
    db.dispose()