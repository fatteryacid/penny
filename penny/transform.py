# ==================================================
# Imports
import pandas pd



# ==================================================
# Functions
def build_dataframe(worksheet, num_split, existing_tid):
    payload = pd.DataFrame(worksheet)

    #Cleanup column names
    container = []
    for i in payload.columns.to_list():
        j = str(i).strip()
        k = (i, j)
        container.append(k)

    clean_names = {k:v for k, v in container}
    payload = payload.rename(clean_names, axis=1)


    payload = payload.drop('per person', axis=1)
    tid = []

    for i in payload.itertuples(): #Build tid codes
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
    pass 


def process_category(df):
    pass 


def process_vendor(df):
    pass 


def process_distribution(df):
    pass 




