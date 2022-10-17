# ==================================================
# Imports
import pandas pd



# ==================================================
# Functions
def build_dataframe(worksheet, existing_tid=None, split_list=None):
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
    tid = []
    
    #Ensure distribution point(s) are integer values
    if split_list != None:
           for name in split_list:
                payload[name] = pd.to_numeric(payload[name], downcast='integer')
    
    #Build TID codes
    for i in payload.itertuples():
        temp = str(i[0])
        temp += str(i[1]).replace('/', '')
        temp += str(i[2]).replace(' ', '').lower()
        temp += str(i[6])
        temp += str(i[7])
        temp += str(i[8])
        
        tid.append(temp)
        
    #Add new col to dataframe
    payload['tid'] = tid
    
    #Check for save state
    if existing_tid == None:
        return payload
    
    else:
        lower_bound = payload.loc[payload['tid'] == existing_tid].index[0]
        return payload.iloc[lower_bound:, :]
        


def process_dates(df):
    pass


def process_item_desc(df):
    df['item'] = df['item'].str.lower().str.strip()


def process_amount(df):
    #Remove undesirable characters
    df['amount'] = df['amount'].replace('$', '')
    df['amount'] = df['amount'].replace(' ', '')
    
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
    pass 


def process_vendor(df):
    pass 


def process_distribution(df):
    pass 




