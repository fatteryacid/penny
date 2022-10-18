# ==================================================
# Imports
import pandas pd
import numpy np 
import uuid



# ==================================================
# Functions
def process_item_desc(df):
    df['item'] = df['item'].str.lower().str.strip()


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


def process_category(df):
    df['category'] = df['category'].str.lower().str.strip()
    df['subcategory'] = df['subcategory'].str.lower().str.strip()
    df['subcategory'] = df['subcategory'].str.replace(' ', '_', regex=False)
    return df


def build_eid(df):
    eid = []
    
    for i in range(len(df)):
        rando = uuid.uuid4().hex
        eid.append(rando)
        
    df['eid'] = eid
    
    return df


def build_dataframe(worksheet, existing_eid=None, split_list=None):
    payload = pd.DataFrame(worksheet)

    #Cleanup column names
    container = []
    for i in payload.columns.to_list():
        j = str(i).strip()
        k = (i, j)
        container.append(k)

    clean_names = {k:v for k, v in container}
    payload = payload.rename(clean_names, axis=1)
    
    #Cleanup empty string imports
    payload = payload.replace('', np.nan)
    payload = payload.dropna()

    #Drop unused column(s)
    payload = payload.drop('per person', axis=1)
    
    #Ensure distribution point(s) are integer values
    if split_list != None:
           for name in split_list:
                payload[name] = pd.to_numeric(payload[name], downcast='integer')
    
    #EID logic
    payload = build_eid(payload)
    
    #Cleanup functions
    payload = process_item_desc(payload)
    payload = process_amount(payload)
    payload = process_category(payload)

    #Check for save state
    if existing_eid == None:
        return payload
    
    else:
        lower_bound = payload.loc[payload['eid'] == existing_eid].index[0]
        return payload.iloc[lower_bound:, :]
        

