# ==================================================
# Imports
import pandas pd
import numpy np 
import uuid



# ==================================================
# Functions
def process_colname(df):
    container = []
    for i in df.columns.to_list():
        j = str(i).strip()
        k = (i, j)
        container.append(k)

    clean_names = {k:v for k, v in container}
    df = df.rename(clean_names, axis=1)
    return df


def process_string(df, target_columns):
    for i in target_columns:
        df[i] = df[i].str.lower()
        df[i] = df[i].str.strip()
            
        if i == 'subcategory':
            df[i] = df[i].str.replace(' ', '_', regex=False)
                
    return df


def process_distribution(df, target_columns):
    for i in target_columns:
        df[i] = pd.to_numeric(df[i], downcast='integer')
    
    return df


def process_amount(df):
    #Remove undesirable characters
    df['amount'] = df['amount'].str.replace('$', '', regex=False)
    df['amount'] = df['amount'].str.replace(' ', '', regex=False)
    
    #Handle negative numbers in accounting format
    temp = []
    
    for i in df.itertuples():
        j = str(i[3])
        
        if '(' in j and ')' in j:
            j = j.replace('(', '')
            j = j.replace(')', '')
            j = '-' + j
            
        temp.append(j)
    
    df['amount'] = temp
    df['amount'] = pd.to_numeric(df['amount'])
    return df


def init_eid(df):
    eid = []
    
    for i in range(len(df)):
        rando = uuid.uuid4().hex
        eid.append(rando)
        
    df['eid'] = eid
    
    return df


def build_dataframe(worksheet, existing_eid=None, split_list=None):
    payload = pd.DataFrame(worksheet)
    
    #Drop unused column(s)
    payload = payload.drop('per person', axis=1)
    

    #EID logic
        #if column does not exist, create it and populate it
        #else, take subset without eids, generate eids for them
        #all cases, commit eid changes to sheet
    

    #Check for save state
    if existing_eid == None:
        return payload
    
    else:
        lower_bound = payload.loc[payload['eid'] == existing_eid].index[0]
        return payload.iloc[lower_bound:, :]
        

