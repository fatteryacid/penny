# ==================================================
# Imports
import pandas pd



# ==================================================
# Functions
def build_dataframe(worksheet, num_split, existing_tid):
    payload = pd.DataFrame(worksheet)
    payload = payload.drop(' per person ', axis=1)
    tid = []

    for i in temp_df.itertuples(): #Build tid codes
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


def process_item_desc(df, location):
    df = df.iloc[:, ]


def process_amount(df):
    pass 


def process_category(df):
    pass 


def process_vendor(df):
    pass 


def process_distribution(df):
    pass 




