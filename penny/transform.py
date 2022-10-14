# ==================================================
# Imports
import pandas pd



# ==================================================
# Functions
def build_dataframe(worksheet, num_split, existing_tid):
    payload = pd.DataFrame(worksheet)
    tid = []

    for i in payload.iterrows():
        tid.append(str(i[0]) + str(i[1]) + str(i[5:5+int(num_split)]))  # tid = concat(date, item desc, split codes)

    if existing_tid != None:    # return subsection if tid exists
        


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




