# ==================================================
# Imports
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import distinct
from sqlalchemy import insert
from sqlalchemy import exc 


# ==================================================
# Functions
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
    
    try:
        with db.connect() as conn:
            result = conn.execute(
                insert(table_object),
                value_list
            )
    except exc.IntegrityError:
        print('WARNING: Attempted to create duplicate data')
        
    db.dispose()

    