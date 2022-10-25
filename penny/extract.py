# ==================================================
# Imports
import pandas as pd
import numpy as np
import gspread as gs
import datetime
import csv



# ==================================================
# Functions
def get_data(sheet_id, ws_loc):
    #Connect to Google service account
    acc = gs.service_account()
    sh = acc.open_by_key(sheet_id)
    ws = sh.get_worksheet(ws_loc)

    #Create backup
    #Example filename 01-01-1991_extract.csv
    filename = '../log/' + datetime.datetime.now().strftime('%m-%d-%Y') + '-backup.csv'
    
    df = pd.DataFrame(ws.get_all_records())
    df = df.replace('', np.nan)
    df = df.dropna()
    
    df.to_csv(filename, index=False)

    #Return records
    return df

