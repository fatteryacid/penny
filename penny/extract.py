# ==================================================
# Imports
import pandas as pd
import gspread as gs
import datetime
import csv



# ==================================================
# Functions
def create_backup(ws):
    #Example filename 01-01-1991_extract.csv
    filename = '../log/' + datetime.datetime.now().strftime('%m-%d-%Y') + '_extract.csv'
    
    df = pd.DataFrame(ws.get_all_records())
    df = df.replace('', np.nan)
    df = df.dropna()
    
    df.to_csv(filename, index=False)

def get_data(sheet_id, ws_loc):
    #Connect to Google service account
    acc = gs.service_account()
    sh = acc.open_by_key(sheet_id)
    ws = sh.get_worksheet(ws_loc)

    #Create backup
    create_backup(ws)

    #Return records
    return ws.get_all_records()

