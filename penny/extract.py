# ==================================================
# Imports
import gspread as gs
import json


# ==================================================
# Functions
def get_data(sheet_id, ws_loc):
    acc = gs.service_account()
    sh = acc.open_by_key(sheet_id)
    ws = sh.get_worksheet(ws_loc)
    return ws.get_all_records()



